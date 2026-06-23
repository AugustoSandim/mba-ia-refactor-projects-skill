from datetime import datetime

from sqlalchemy.orm import joinedload

from database import db
from models.task import Task
from models.user import User
from models.category import Category


def _parse_due_date(due_date):
    if not due_date:
        return None
    return datetime.strptime(due_date, "%Y-%m-%d")


def _task_with_context(task):
    data = task.to_dict()
    data["overdue"] = task.is_overdue()
    data["user_name"] = task.user.name if task.user else None
    data["category_name"] = task.category.name if task.category else None
    return data


def get_tasks():
    tasks = (
        db.session.query(Task)
        .options(joinedload(Task.user), joinedload(Task.category))
        .all()
    )
    return [_task_with_context(task) for task in tasks], 200


def get_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return {"error": "Task não encontrada"}, 404
    data = _task_with_context(task)
    return data, 200


def create_task(payload):
    if not payload:
        return {"error": "Dados inválidos"}, 400

    title = payload.get("title")
    if not title:
        return {"error": "Título é obrigatório"}, 400
    if len(title) < 3:
        return {"error": "Título muito curto"}, 400
    if len(title) > 200:
        return {"error": "Título muito longo"}, 400

    status = payload.get("status", "pending")
    priority = payload.get("priority", 3)
    if status not in ["pending", "in_progress", "done", "cancelled"]:
        return {"error": "Status inválido"}, 400
    if priority < 1 or priority > 5:
        return {"error": "Prioridade deve ser entre 1 e 5"}, 400

    user_id = payload.get("user_id")
    category_id = payload.get("category_id")
    if user_id and not db.session.get(User, user_id):
        return {"error": "Usuário não encontrado"}, 404
    if category_id and not db.session.get(Category, category_id):
        return {"error": "Categoria não encontrada"}, 404

    task = Task(
        title=title,
        description=payload.get("description", ""),
        status=status,
        priority=priority,
        user_id=user_id,
        category_id=category_id,
        tags=",".join(payload["tags"]) if isinstance(payload.get("tags"), list) else payload.get("tags"),
    )
    try:
        task.due_date = _parse_due_date(payload.get("due_date"))
    except ValueError:
        return {"error": "Formato de data inválido. Use YYYY-MM-DD"}, 400

    try:
        db.session.add(task)
        db.session.commit()
        return task.to_dict(), 201
    except Exception:
        db.session.rollback()
        return {"error": "Erro ao criar task"}, 500


def update_task(task_id, payload):
    task = db.session.get(Task, task_id)
    if not task:
        return {"error": "Task não encontrada"}, 404
    if not payload:
        return {"error": "Dados inválidos"}, 400

    if "title" in payload:
        if len(payload["title"]) < 3:
            return {"error": "Título muito curto"}, 400
        if len(payload["title"]) > 200:
            return {"error": "Título muito longo"}, 400
        task.title = payload["title"]
    if "description" in payload:
        task.description = payload["description"]
    if "status" in payload:
        if payload["status"] not in ["pending", "in_progress", "done", "cancelled"]:
            return {"error": "Status inválido"}, 400
        task.status = payload["status"]
    if "priority" in payload:
        if payload["priority"] < 1 or payload["priority"] > 5:
            return {"error": "Prioridade deve ser entre 1 e 5"}, 400
        task.priority = payload["priority"]
    if "user_id" in payload:
        if payload["user_id"] and not db.session.get(User, payload["user_id"]):
            return {"error": "Usuário não encontrado"}, 404
        task.user_id = payload["user_id"]
    if "category_id" in payload:
        if payload["category_id"] and not db.session.get(Category, payload["category_id"]):
            return {"error": "Categoria não encontrada"}, 404
        task.category_id = payload["category_id"]
    if "due_date" in payload:
        try:
            task.due_date = _parse_due_date(payload["due_date"])
        except ValueError:
            return {"error": "Formato de data inválido"}, 400
    if "tags" in payload:
        task.tags = ",".join(payload["tags"]) if isinstance(payload["tags"], list) else payload["tags"]

    task.updated_at = datetime.utcnow()
    try:
        db.session.commit()
        return task.to_dict(), 200
    except Exception:
        db.session.rollback()
        return {"error": "Erro ao atualizar"}, 500


def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return {"error": "Task não encontrada"}, 404
    try:
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deletada com sucesso"}, 200
    except Exception:
        db.session.rollback()
        return {"error": "Erro ao deletar"}, 500


def search_tasks(query, status, priority, user_id):
    tasks = db.session.query(Task)
    if query:
        tasks = tasks.filter(db.or_(Task.title.like(f"%{query}%"), Task.description.like(f"%{query}%")))
    if status:
        tasks = tasks.filter(Task.status == status)
    if priority:
        tasks = tasks.filter(Task.priority == int(priority))
    if user_id:
        tasks = tasks.filter(Task.user_id == int(user_id))
    results = tasks.all()
    return [task.to_dict() for task in results], 200


def task_stats():
    total = Task.query.count()
    pending = Task.query.filter_by(status="pending").count()
    in_progress = Task.query.filter_by(status="in_progress").count()
    done = Task.query.filter_by(status="done").count()
    cancelled = Task.query.filter_by(status="cancelled").count()
    overdue = Task.query.filter(
        Task.due_date.isnot(None),
        Task.due_date < datetime.utcnow(),
        Task.status.notin_(["done", "cancelled"]),
    ).count()

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "done": done,
        "cancelled": cancelled,
        "overdue": overdue,
        "completion_rate": round((done / total) * 100, 2) if total > 0 else 0,
    }, 200

