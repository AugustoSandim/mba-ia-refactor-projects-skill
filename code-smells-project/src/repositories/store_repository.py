from src.database.connection import get_db


class StoreRepository:
    def list_products(self):
        rows = get_db().execute("SELECT * FROM produtos").fetchall()
        return [dict(row) for row in rows]

    def get_product(self, product_id):
        row = get_db().execute("SELECT * FROM produtos WHERE id = ?", (product_id,)).fetchone()
        return dict(row) if row else None

    def create_product(self, payload):
        cursor = get_db().cursor()
        cursor.execute(
            """
            INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload["nome"],
                payload.get("descricao", ""),
                payload["preco"],
                payload["estoque"],
                payload.get("categoria", "geral"),
            ),
        )
        get_db().commit()
        return cursor.lastrowid

    def update_product(self, product_id, payload):
        get_db().execute(
            """
            UPDATE produtos
            SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ?
            WHERE id = ?
            """,
            (
                payload["nome"],
                payload.get("descricao", ""),
                payload["preco"],
                payload["estoque"],
                payload.get("categoria", "geral"),
                product_id,
            ),
        )
        get_db().commit()

    def delete_product(self, product_id):
        get_db().execute("DELETE FROM produtos WHERE id = ?", (product_id,))
        get_db().commit()

    def search_products(self, term="", category=None, min_price=None, max_price=None):
        query = "SELECT * FROM produtos WHERE 1=1"
        params = []
        if term:
            query += " AND (nome LIKE ? OR descricao LIKE ?)"
            like_term = f"%{term}%"
            params.extend([like_term, like_term])
        if category:
            query += " AND categoria = ?"
            params.append(category)
        if min_price is not None:
            query += " AND preco >= ?"
            params.append(min_price)
        if max_price is not None:
            query += " AND preco <= ?"
            params.append(max_price)
        rows = get_db().execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def list_users(self):
        rows = get_db().execute(
            "SELECT id, nome, email, tipo, criado_em FROM usuarios"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_user(self, user_id):
        row = get_db().execute(
            "SELECT id, nome, email, tipo, criado_em FROM usuarios WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None

    def get_user_with_password(self, email):
        row = get_db().execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None

    def create_user(self, name, email, password_hash, user_type="cliente"):
        cursor = get_db().cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, user_type),
        )
        get_db().commit()
        return cursor.lastrowid

    def create_order(self, user_id, items):
        db = get_db()
        cursor = db.cursor()
        total = 0.0
        priced_items = []

        for item in items:
            product = cursor.execute(
                "SELECT id, nome, preco, estoque FROM produtos WHERE id = ?",
                (item["produto_id"],),
            ).fetchone()
            if not product:
                raise ValueError(f"Produto {item['produto_id']} não encontrado")
            if product["estoque"] < item["quantidade"]:
                raise ValueError(f"Estoque insuficiente para {product['nome']}")
            unit_price = float(product["preco"])
            total += unit_price * item["quantidade"]
            priced_items.append(
                {
                    "produto_id": item["produto_id"],
                    "quantidade": item["quantidade"],
                    "preco_unitario": unit_price,
                }
            )

        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (user_id, total),
        )
        order_id = cursor.lastrowid

        for item in priced_items:
            cursor.execute(
                """
                INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
                """,
                (order_id, item["produto_id"], item["quantidade"], item["preco_unitario"]),
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], item["produto_id"]),
            )

        db.commit()
        return {"pedido_id": order_id, "total": round(total, 2)}

    def list_orders(self, user_id=None):
        db = get_db()
        if user_id:
            order_rows = db.execute(
                "SELECT * FROM pedidos WHERE usuario_id = ? ORDER BY id DESC",
                (user_id,),
            ).fetchall()
        else:
            order_rows = db.execute("SELECT * FROM pedidos ORDER BY id DESC").fetchall()

        if not order_rows:
            return []

        order_ids = [row["id"] for row in order_rows]
        placeholders = ",".join(["?"] * len(order_ids))
        item_rows = db.execute(
            f"""
            SELECT i.pedido_id, i.produto_id, i.quantidade, i.preco_unitario, p.nome AS produto_nome
            FROM itens_pedido i
            JOIN produtos p ON p.id = i.produto_id
            WHERE i.pedido_id IN ({placeholders})
            ORDER BY i.id
            """,
            order_ids,
        ).fetchall()

        items_by_order = {}
        for item in item_rows:
            items_by_order.setdefault(item["pedido_id"], []).append(
                {
                    "produto_id": item["produto_id"],
                    "produto_nome": item["produto_nome"],
                    "quantidade": item["quantidade"],
                    "preco_unitario": item["preco_unitario"],
                }
            )

        orders = []
        for row in order_rows:
            order = dict(row)
            order["itens"] = items_by_order.get(row["id"], [])
            orders.append(order)
        return orders

    def update_order_status(self, order_id, status):
        get_db().execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, order_id))
        get_db().commit()

    def report_sales(self):
        db = get_db()
        total_orders = db.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
        gross_revenue = db.execute("SELECT COALESCE(SUM(total), 0) FROM pedidos").fetchone()[0]
        pending = db.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'").fetchone()[0]
        approved = db.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'").fetchone()[0]
        cancelled = db.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'").fetchone()[0]

        discount = 0
        if gross_revenue > 10000:
            discount = gross_revenue * 0.1
        elif gross_revenue > 5000:
            discount = gross_revenue * 0.05
        elif gross_revenue > 1000:
            discount = gross_revenue * 0.02

        return {
            "total_pedidos": total_orders,
            "faturamento_bruto": round(gross_revenue, 2),
            "desconto_aplicavel": round(discount, 2),
            "faturamento_liquido": round(gross_revenue - discount, 2),
            "pedidos_pendentes": pending,
            "pedidos_aprovados": approved,
            "pedidos_cancelados": cancelled,
            "ticket_medio": round(gross_revenue / total_orders, 2) if total_orders > 0 else 0,
        }

    def health_snapshot(self):
        db = get_db()
        db.execute("SELECT 1")
        products = db.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
        users = db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
        orders = db.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
        return {"produtos": products, "usuarios": users, "pedidos": orders}

