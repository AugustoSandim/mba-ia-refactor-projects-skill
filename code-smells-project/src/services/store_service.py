from werkzeug.security import generate_password_hash, check_password_hash
from src.repositories.store_repository import StoreRepository


class StoreService:
    VALID_CATEGORIES = {"informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"}
    VALID_ORDER_STATUS = {"pendente", "aprovado", "enviado", "entregue", "cancelado"}

    def __init__(self, repository=None):
        self.repository = repository or StoreRepository()

    def list_products(self):
        return self.repository.list_products()

    def get_product(self, product_id):
        return self.repository.get_product(product_id)

    def create_product(self, payload):
        self._validate_product_payload(payload)
        return self.repository.create_product(payload)

    def update_product(self, product_id, payload):
        existing = self.repository.get_product(product_id)
        if not existing:
            return None
        self._validate_product_payload(payload)
        self.repository.update_product(product_id, payload)
        return True

    def delete_product(self, product_id):
        existing = self.repository.get_product(product_id)
        if not existing:
            return False
        self.repository.delete_product(product_id)
        return True

    def search_products(self, term, category, min_price, max_price):
        return self.repository.search_products(term, category, min_price, max_price)

    def list_users(self):
        return self.repository.list_users()

    def get_user(self, user_id):
        return self.repository.get_user(user_id)

    def create_user(self, payload):
        name = payload.get("nome", "").strip()
        email = payload.get("email", "").strip().lower()
        password = payload.get("senha", "")
        if not name or not email or not password:
            raise ValueError("Nome, email e senha são obrigatórios")
        password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        user_id = self.repository.create_user(name, email, password_hash)
        return user_id

    def login(self, payload):
        email = payload.get("email", "").strip().lower()
        password = payload.get("senha", "")
        if not email or not password:
            raise ValueError("Email e senha são obrigatórios")
        user = self.repository.get_user_with_password(email)
        if not user:
            return None
        try:
            password_valid = check_password_hash(user["senha"], password)
        except ValueError:
            password_valid = user["senha"] == password
        if not password_valid:
            return None
        return {"id": user["id"], "nome": user["nome"], "email": user["email"], "tipo": user["tipo"]}

    def create_order(self, payload):
        user_id = payload.get("usuario_id")
        items = payload.get("itens", [])
        if not user_id:
            raise ValueError("Usuario ID é obrigatório")
        if not items:
            raise ValueError("Pedido deve ter pelo menos 1 item")
        return self.repository.create_order(user_id, items)

    def list_orders_by_user(self, user_id):
        return self.repository.list_orders(user_id=user_id)

    def list_orders(self):
        return self.repository.list_orders()

    def update_order_status(self, order_id, payload):
        status = payload.get("status", "")
        if status not in self.VALID_ORDER_STATUS:
            raise ValueError("Status inválido")
        self.repository.update_order_status(order_id, status)
        return status

    def sales_report(self):
        return self.repository.report_sales()

    def health(self):
        return self.repository.health_snapshot()

    def _validate_product_payload(self, payload):
        required = ("nome", "preco", "estoque")
        for field in required:
            if field not in payload:
                raise ValueError(f"{field.capitalize()} é obrigatório")

        name = payload["nome"]
        price = payload["preco"]
        stock = payload["estoque"]
        category = payload.get("categoria", "geral")

        if len(name) < 2:
            raise ValueError("Nome muito curto")
        if len(name) > 200:
            raise ValueError("Nome muito longo")
        if price < 0:
            raise ValueError("Preço não pode ser negativo")
        if stock < 0:
            raise ValueError("Estoque não pode ser negativo")
        if category not in self.VALID_CATEGORIES:
            raise ValueError(f"Categoria inválida. Válidas: {sorted(self.VALID_CATEGORIES)}")

