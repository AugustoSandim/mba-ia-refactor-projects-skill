from database import db
from models.category import Category
from models.task import Task


def get_categories():
    categories = Category.query.all()
    response = []
    for category in categories:
        data = category.to_dict()
        data["task_count"] = Task.query.filter_by(category_id=category.id).count()
        response.append(data)
    return response, 200


def create_category(payload):
    if not payload:
        return {"error": "Dados inválidos"}, 400
    if not payload.get("name"):
        return {"error": "Nome é obrigatório"}, 400

    category = Category(
        name=payload["name"],
        description=payload.get("description", ""),
        color=payload.get("color", "#000000"),
    )
    try:
        db.session.add(category)
        db.session.commit()
        return category.to_dict(), 201
    except Exception:
        db.session.rollback()
        return {"error": "Erro ao criar categoria"}, 500


def update_category(category_id, payload):
    category = db.session.get(Category, category_id)
    if not category:
        return {"error": "Categoria não encontrada"}, 404

    if "name" in payload:
        category.name = payload["name"]
    if "description" in payload:
        category.description = payload["description"]
    if "color" in payload:
        category.color = payload["color"]

    try:
        db.session.commit()
        return category.to_dict(), 200
    except Exception:
        db.session.rollback()
        return {"error": "Erro ao atualizar"}, 500


def delete_category(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        return {"error": "Categoria não encontrada"}, 404

    try:
        db.session.delete(category)
        db.session.commit()
        return {"message": "Categoria deletada"}, 200
    except Exception:
        db.session.rollback()
        return {"error": "Erro ao deletar"}, 500

