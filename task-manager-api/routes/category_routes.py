from flask import Blueprint, request, jsonify

from controllers import category_controller


category_bp = Blueprint("categories", __name__)


@category_bp.route("/categories", methods=["GET"])
def get_categories():
    data, status = category_controller.get_categories()
    return jsonify(data), status


@category_bp.route("/categories", methods=["POST"])
def create_category():
    data, status = category_controller.create_category(request.get_json())
    return jsonify(data), status


@category_bp.route("/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data, status = category_controller.update_category(category_id, request.get_json() or {})
    return jsonify(data), status


@category_bp.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    data, status = category_controller.delete_category(category_id)
    return jsonify(data), status

