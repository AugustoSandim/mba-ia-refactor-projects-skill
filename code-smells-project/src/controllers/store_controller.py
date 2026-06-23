from src.services.store_service import StoreService


class StoreController:
    def __init__(self, service=None):
        self.service = service or StoreService()

    def list_products(self):
        return {"dados": self.service.list_products(), "sucesso": True}, 200

    def get_product(self, product_id):
        product = self.service.get_product(product_id)
        if not product:
            return {"erro": "Produto não encontrado", "sucesso": False}, 404
        return {"dados": product, "sucesso": True}, 200

    def create_product(self, payload):
        product_id = self.service.create_product(payload)
        return {"dados": {"id": product_id}, "sucesso": True, "mensagem": "Produto criado"}, 201

    def update_product(self, product_id, payload):
        updated = self.service.update_product(product_id, payload)
        if not updated:
            return {"erro": "Produto não encontrado"}, 404
        return {"sucesso": True, "mensagem": "Produto atualizado"}, 200

    def delete_product(self, product_id):
        deleted = self.service.delete_product(product_id)
        if not deleted:
            return {"erro": "Produto não encontrado"}, 404
        return {"sucesso": True, "mensagem": "Produto deletado"}, 200

    def search_products(self, term, category, min_price, max_price):
        data = self.service.search_products(term, category, min_price, max_price)
        return {"dados": data, "total": len(data), "sucesso": True}, 200

    def list_users(self):
        return {"dados": self.service.list_users(), "sucesso": True}, 200

    def get_user(self, user_id):
        user = self.service.get_user(user_id)
        if not user:
            return {"erro": "Usuário não encontrado"}, 404
        return {"dados": user, "sucesso": True}, 200

    def create_user(self, payload):
        user_id = self.service.create_user(payload)
        return {"dados": {"id": user_id}, "sucesso": True}, 201

    def login(self, payload):
        user = self.service.login(payload)
        if not user:
            return {"erro": "Email ou senha inválidos", "sucesso": False}, 401
        return {"dados": user, "sucesso": True, "mensagem": "Login OK"}, 200

    def create_order(self, payload):
        order_result = self.service.create_order(payload)
        return {"dados": order_result, "sucesso": True, "mensagem": "Pedido criado com sucesso"}, 201

    def list_orders_by_user(self, user_id):
        return {"dados": self.service.list_orders_by_user(user_id), "sucesso": True}, 200

    def list_orders(self):
        return {"dados": self.service.list_orders(), "sucesso": True}, 200

    def update_order_status(self, order_id, payload):
        status = self.service.update_order_status(order_id, payload)
        return {"sucesso": True, "mensagem": "Status atualizado", "status": status}, 200

    def sales_report(self):
        return {"dados": self.service.sales_report(), "sucesso": True}, 200

    def health_check(self):
        return {"status": "ok", "database": "connected", "counts": self.service.health(), "versao": "2.0.0"}, 200

