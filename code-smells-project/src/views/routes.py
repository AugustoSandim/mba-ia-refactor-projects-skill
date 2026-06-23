from functools import wraps
from flask import Blueprint, current_app, jsonify, request

from src.controllers.store_controller import StoreController
from src.database.connection import get_db
from src.database.schema import reset_data


api_bp = Blueprint("api", __name__)
controller = StoreController()


def require_admin_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-Admin-Token", "")
        if token != current_app.config["ADMIN_TOKEN"]:
            return jsonify({"erro": "Acesso negado", "sucesso": False}), 403
        return func(*args, **kwargs)

    return wrapper


@api_bp.get("/")
def index():
    return jsonify(
        {
            "mensagem": "Bem-vindo à API da Loja",
            "versao": "2.0.0",
            "endpoints": {
                "produtos": "/produtos",
                "usuarios": "/usuarios",
                "pedidos": "/pedidos",
                "login": "/login",
                "relatorios": "/relatorios/vendas",
                "health": "/health",
            },
        }
    )


@api_bp.get("/health")
def health():
    data, status = controller.health_check()
    return jsonify(data), status


@api_bp.get("/produtos")
def list_products():
    data, status = controller.list_products()
    return jsonify(data), status


@api_bp.get("/produtos/busca")
def search_products():
    min_price = request.args.get("preco_min")
    max_price = request.args.get("preco_max")
    data, status = controller.search_products(
        request.args.get("q", ""),
        request.args.get("categoria"),
        float(min_price) if min_price else None,
        float(max_price) if max_price else None,
    )
    return jsonify(data), status


@api_bp.get("/produtos/<int:product_id>")
def get_product(product_id):
    data, status = controller.get_product(product_id)
    return jsonify(data), status


@api_bp.post("/produtos")
def create_product():
    data, status = controller.create_product(request.get_json() or {})
    return jsonify(data), status


@api_bp.put("/produtos/<int:product_id>")
def update_product(product_id):
    data, status = controller.update_product(product_id, request.get_json() or {})
    return jsonify(data), status


@api_bp.delete("/produtos/<int:product_id>")
def delete_product(product_id):
    data, status = controller.delete_product(product_id)
    return jsonify(data), status


@api_bp.get("/usuarios")
def list_users():
    data, status = controller.list_users()
    return jsonify(data), status


@api_bp.get("/usuarios/<int:user_id>")
def get_user(user_id):
    data, status = controller.get_user(user_id)
    return jsonify(data), status


@api_bp.post("/usuarios")
def create_user():
    data, status = controller.create_user(request.get_json() or {})
    return jsonify(data), status


@api_bp.post("/login")
def login():
    data, status = controller.login(request.get_json() or {})
    return jsonify(data), status


@api_bp.post("/pedidos")
def create_order():
    data, status = controller.create_order(request.get_json() or {})
    return jsonify(data), status


@api_bp.get("/pedidos")
def list_orders():
    data, status = controller.list_orders()
    return jsonify(data), status


@api_bp.get("/pedidos/usuario/<int:user_id>")
def list_orders_by_user(user_id):
    data, status = controller.list_orders_by_user(user_id)
    return jsonify(data), status


@api_bp.put("/pedidos/<int:order_id>/status")
def update_order_status(order_id):
    data, status = controller.update_order_status(order_id, request.get_json() or {})
    return jsonify(data), status


@api_bp.get("/relatorios/vendas")
def sales_report():
    data, status = controller.sales_report()
    return jsonify(data), status


@api_bp.post("/admin/reset-db")
@require_admin_token
def reset_database():
    reset_data()
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200


@api_bp.post("/admin/query")
@require_admin_token
def execute_query():
    payload = request.get_json() or {}
    query = payload.get("sql", "").strip()
    if not query:
        return jsonify({"erro": "Query não informada"}), 400
    if not query.upper().startswith("SELECT"):
        return jsonify({"erro": "Apenas consultas SELECT são permitidas"}), 400

    rows = get_db().execute(query).fetchall()
    return jsonify({"dados": [dict(row) for row in rows], "sucesso": True}), 200

