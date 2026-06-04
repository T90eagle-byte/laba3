from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user

from app.pharmacy import (
    DBStorage,
    OrderItem,
    hash_password,
    product_image_filename,
    verify_password,
)


api_bp = Blueprint("api", __name__, url_prefix="/api")
DEFAULT_PAYMENT = "\u043d\u0430\u043b\u0438\u0447\u043d\u044b\u0435"


def api_ok(data=None, status=200):
    return jsonify({"ok": True, "data": data}), status


def api_error(message, status=400):
    return jsonify({"ok": False, "error": str(message)}), status


def serialize_product(product):
    return {
        "id": product.id,
        "name": product.name,
        "dosage": product.dosage,
        "category": product.category,
        "price": product.price,
        "in_stock": bool(product.in_stock),
        "image": product_image_filename(product),
    }


def serialize_user(user):
    return {
        "id": user.id,
        "login": user.login,
        "name": user.name,
        "surname": user.surname,
        "patronymic": user.patronymic,
        "address": user.address,
        "is_admin": bool(user.is_admin),
    }


def get_storage():
    return DBStorage()


def is_current_user_admin():
    return bool(getattr(current_user, "is_admin", 0))


def require_api_login():
    if not current_user.is_authenticated:
        return api_error("Authentication required", 401)
    return None


def get_json_payload():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, api_error("Invalid JSON body", 400)
    return payload, None


def parse_product_ids(payload):
    product_ids = payload.get("product_ids")
    if not isinstance(product_ids, list) or not product_ids:
        return None, api_error("product_ids must be a non-empty list", 400)

    parsed_ids = []
    for raw_id in product_ids:
        try:
            product_id = int(raw_id)
        except (TypeError, ValueError):
            return None, api_error("product_ids must contain product ids", 400)
        if product_id <= 0:
            return None, api_error("product_ids must contain product ids", 400)
        parsed_ids.append(product_id)
    return parsed_ids, None


def build_order_items(storage, product_ids):
    items = []
    for product_id in product_ids:
        product = storage.GetProduct(product_id)
        if not product.id:
            return None, api_error(f"Product not found: {product_id}", 404)
        if not product.in_stock:
            return None, api_error(f"Product is not available: {product_id}", 400)
        items.append({
            "name": product.name,
            "dosage": product.dosage,
            "price": product.price,
        })
    return items, None


def find_product_snapshot(storage, name, dosage):
    cursor = storage.db.cursor()
    cursor.execute(
        "SELECT * FROM products WHERE name=? AND dosage=? LIMIT 1",
        (name, dosage),
    )
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row["id"],
        "name": row["name"],
        "dosage": row["dosage"],
        "category": row["category"],
        "price": row["price"],
        "in_stock": bool(row["in_stock"]),
    }


def serialize_order_item(item, storage):
    name = item.get("name", "")
    dosage = item.get("dosage", "")
    price = item.get("price", 0)
    product = find_product_snapshot(storage, name, dosage)

    if product:
        return {
            "id": product["id"],
            "name": product["name"],
            "dosage": product["dosage"],
            "category": product["category"],
            "price": price,
            "in_stock": product["in_stock"],
            "image": product_image_filename(product),
        }

    return {
        "id": None,
        "name": name,
        "dosage": dosage,
        "category": "",
        "price": price,
        "in_stock": False,
        "image": product_image_filename(name=name),
    }


def serialize_order(order, storage):
    items = [serialize_order_item(item, storage) for item in order.items]
    return {
        "id": order.id,
        "user_id": order.user_id,
        "payment": order.payment,
        "created": str(order.created),
        "items": items,
        "total": sum(item["price"] for item in items),
    }


def get_all_orders(storage):
    cursor = storage.db.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    for row in cursor.fetchall():
        order = OrderItem()
        order.DBLoad(row, storage.db.cursor())
        yield order


def get_accessible_order(storage, order_id):
    order = storage.GetOrder(order_id)
    if not order.id:
        return None, api_error("Order not found", 404)
    if not is_current_user_admin() and order.user_id != int(current_user.get_id()):
        return None, api_error("Order access denied", 403)
    return order, None


@api_bp.post("/auth/login")
def api_login():
    payload = request.get_json(silent=True) or {}
    login = (payload.get("login") or "").strip()
    password = payload.get("password") or ""

    storage = get_storage()
    try:
        user = storage.GetUserByLogin(login) if login else None
        if not user:
            return api_error("Invalid login or password", 401)

        is_valid, needs_rehash = verify_password(user.password_hash, password)
        if not is_valid:
            return api_error("Invalid login or password", 401)

        if needs_rehash:
            new_hash = hash_password(password)
            storage.UpdatePassword(user.id, new_hash)
            storage.db.commit()
            user.password_hash = new_hash

        login_user(user)
        return api_ok({"user": serialize_user(user)})
    finally:
        storage.db.close()


@api_bp.post("/auth/logout")
def api_logout():
    if current_user.is_authenticated:
        logout_user()
    return api_ok({"logged_out": True})


@api_bp.get("/auth/me")
def api_me():
    if not current_user.is_authenticated:
        return api_error("Authentication required", 401)
    return api_ok({"user": serialize_user(current_user)})


@api_bp.get("/orders")
def api_orders():
    auth_error = require_api_login()
    if auth_error:
        return auth_error

    storage = get_storage()
    try:
        if is_current_user_admin():
            orders = list(get_all_orders(storage))
        else:
            orders = list(storage.GetUserOrders(int(current_user.get_id())))
        return api_ok([serialize_order(order, storage) for order in orders])
    finally:
        storage.db.close()


@api_bp.post("/orders")
def api_create_order():
    auth_error = require_api_login()
    if auth_error:
        return auth_error

    payload, json_error = get_json_payload()
    if json_error:
        return json_error

    product_ids, ids_error = parse_product_ids(payload)
    if ids_error:
        return ids_error

    storage = get_storage()
    try:
        items, items_error = build_order_items(storage, product_ids)
        if items_error:
            return items_error

        payment = (payload.get("payment") or DEFAULT_PAYMENT).strip() or DEFAULT_PAYMENT
        order = OrderItem(
            user_id=int(current_user.get_id()),
            payment=payment,
            items=items,
        )
        storage.AddOrder(order)
        storage.db.commit()
        created = storage.GetOrder(order.id)
        return api_ok(serialize_order(created, storage), 201)
    finally:
        storage.db.close()


@api_bp.get("/orders/<int:order_id>")
def api_order_detail(order_id):
    auth_error = require_api_login()
    if auth_error:
        return auth_error

    storage = get_storage()
    try:
        order, access_error = get_accessible_order(storage, order_id)
        if access_error:
            return access_error
        return api_ok(serialize_order(order, storage))
    finally:
        storage.db.close()


@api_bp.put("/orders/<int:order_id>")
def api_update_order(order_id):
    auth_error = require_api_login()
    if auth_error:
        return auth_error

    payload, json_error = get_json_payload()
    if json_error:
        return json_error

    product_ids, ids_error = parse_product_ids(payload)
    if ids_error:
        return ids_error

    storage = get_storage()
    try:
        order, access_error = get_accessible_order(storage, order_id)
        if access_error:
            return access_error

        items, items_error = build_order_items(storage, product_ids)
        if items_error:
            return items_error

        payment = (payload.get("payment") or order.payment or DEFAULT_PAYMENT).strip()
        order.payment = payment or DEFAULT_PAYMENT
        order.items = items
        storage.AddOrder(order)
        storage.db.commit()
        updated = storage.GetOrder(order.id)
        return api_ok(serialize_order(updated, storage))
    finally:
        storage.db.close()


@api_bp.delete("/orders/<int:order_id>")
def api_delete_order(order_id):
    auth_error = require_api_login()
    if auth_error:
        return auth_error

    storage = get_storage()
    try:
        order, access_error = get_accessible_order(storage, order_id)
        if access_error:
            return access_error

        storage.DeleteOrder(order.id)
        storage.db.commit()
        return api_ok({"deleted": True, "id": order.id})
    finally:
        storage.db.close()


@api_bp.get("/products")
def api_products():
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    storage = get_storage()
    try:
        products = [
            serialize_product(product)
            for product in storage.GetProducts(query=query, category=category)
        ]
        return api_ok(products)
    finally:
        storage.db.close()


@api_bp.get("/products/<int:product_id>")
def api_product_detail(product_id):
    storage = get_storage()
    try:
        product = storage.GetProduct(product_id)
        if not product.id:
            return api_error("Product not found", 404)
        return api_ok(serialize_product(product))
    finally:
        storage.db.close()
