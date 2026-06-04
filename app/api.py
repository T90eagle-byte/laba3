from flask import Blueprint, jsonify, request

from app.pharmacy import DBStorage, product_image_filename


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


def get_storage():
    return DBStorage()


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
