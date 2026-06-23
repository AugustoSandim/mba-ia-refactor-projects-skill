import re

from database import db
from models.user import User
from models.task import Task


def get_users():
    users = User.query.all()
    response = []
    for user in users:
        data = user.to_dict()
        data["task_count"] = len(user.tasks)
        response.append(data)
    return response, 200


def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "Usuário não encontrado"}, 404
    data = user.to_dict()
    data["tasks"] = [task.to_dict() for task in user.tasks]
    return data, 200


def create_user(payload):
    if not payload:
        return {"error": "Dados inválidos"}, 400

    name = payload.get("name")
    email = payload.get("email")
    password = payload.get("password")
    role = payload.get("role", "user")

    if not name:
        return {"error": "Nome é obrigatório"}, 400
    if not email:
        return {"error": "Email é obrigatório"}, 400
    if not password:
        return {"error": "Senha é obrigatória"}, 400
    if not re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email):
        return {"error": "Email inválido"}, 400
    if len(password) < 4:
        return {"error": "Senha deve ter no mínimo 4 caracteres"}, 400
    if role not in ["user", "admin", "manager"]:
        return {"error": "Role inválido"}, 400
    if User.query.filter_by(email=email).first():
        return {"error": "Email já cadastrado"}, 409

    user = User(name=name, email=email, role=role)
    user.set_password(password)
    try:
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
    except Exception:
        db.session.rollback()
        return {"error": "Erro ao criar usuário"}, 500


def update_user(user_id, payload):
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "Usuário não encontrado"}, 404
    if not payload:
        return {"error": "Dados inválidos"}, 400

    if "name" in payload:
        user.name = payload["name"]
    if "email" in payload:
        if not re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", payload["email"]):
            return {"error": "Email inválido"}, 400
        existing = User.query.filter_by(email=payload["email"]).first()
        if existing and existing.id != user.id:
            return {"error": "Email já cadastrado"}, 409
        user.email = payload["email"]
    if "password" in payload:
        if len(payload["password"]) < 4:
            return {"error": "Senha muito curta"}, 400
        user.set_password(payload["password"])
    if "role" in payload:
        if payload["role"] not in ["user", "admin", "manager"]:
            return {"error": "Role inválido"}, 400
        user.role = payload["role"]
    if "active" in payload:
        user.active = payload["active"]

    try:
        db.session.commit()
        return user.to_dict(), 200
    except Exception:
        db.session.rollback()
        return {"error": "Erro ao atualizar"}, 500


def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "Usuário não encontrado"}, 404
    for task in Task.query.filter_by(user_id=user_id).all():
        db.session.delete(task)
    try:
        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuário deletado com sucesso"}, 200
    except Exception:
        db.session.rollback()
        return {"error": "Erro ao deletar"}, 500


def get_user_tasks(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "Usuário não encontrado"}, 404
    response = []
    for task in Task.query.filter_by(user_id=user_id).all():
        data = task.to_dict()
        data["overdue"] = task.is_overdue()
        response.append(data)
    return response, 200


def login(payload):
    if not payload:
        return {"error": "Dados inválidos"}, 400
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        return {"error": "Email e senha são obrigatórios"}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"error": "Credenciais inválidas"}, 401
    if not user.active:
        return {"error": "Usuário inativo"}, 403

    return {
        "message": "Login realizado com sucesso",
        "user": user.to_dict(),
        "token": f"fake-jwt-token-{user.id}",
    }, 200

