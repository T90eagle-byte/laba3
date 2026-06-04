from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user

from app.pharmacy import (
    DBStorage,
    hash_password,
    product_image_filename,
    verify_password,
)


api_bp = Blueprint("api", __name__, url_prefix="/api")


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
