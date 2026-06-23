# Refactoring Playbook

Padrões concretos de transformação com exemplos before/after.

## 1) Extract Hardcoded Config to Environment

**Problema**: segredo hardcoded no código.  
**Alvo**: módulo `config`.

```python
# Before
app.config["SECRET_KEY"] = "super-secret"
```

```python
# After
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
```

## 2) Replace String SQL with Parameterized Query

**Problema**: SQL injection por concatenação.

```python
# Before
cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
```

```python
# After
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

## 3) Split God Class into Route + Controller + Service

**Problema**: uma classe concentra tudo.

```javascript
// Before
app.post("/checkout", (req, res) => {
  // validação + regra + db + resposta
});
```

```javascript
// After
router.post("/checkout", checkoutController.checkout);
// controller -> service -> repository
```

## 4) Move Business Logic Out of Route Handler

**Problema**: regra de domínio na rota.

```python
# Before
@bp.route("/tasks", methods=["POST"])
def create_task():
    # validações e regras complexas
```

```python
# After
@bp.route("/tasks", methods=["POST"])
def create_task():
    return task_controller.create_task()
```

## 5) Introduce Error Handling Middleware

**Problema**: tratamento inconsistente de erro.

```javascript
// Before
try { ... } catch (e) { res.status(500).send("Erro"); }
```

```javascript
// After
next(error); // middleware central traduz erro para resposta HTTP
```

## 6) Replace Weak Password Hash

**Problema**: MD5/custom hash para senha.

```python
# Before
hashlib.md5(password.encode()).hexdigest()
```

```python
# After
generate_password_hash(password)
check_password_hash(stored, password)
```

## 7) Remove N+1 Query with Join/Eager Loading

**Problema**: query em loop.

```python
# Before
for order in orders:
    items = query_items(order.id)
```

```python
# After
orders = query_orders_with_items_join()
```

## 8) Replace Global Mutable Singleton with Factory

**Problema**: estado global compartilhado.

```python
# Before
db_connection = None
```

```python
# After
def get_connection():
    return sqlite3.connect(path)
```

## 9) Extract Route Registration to Views Module

**Problema**: rotas espalhadas no entrypoint.

```python
# Before
app.add_url_rule(...)
app.route(...)
```

```python
# After
app.register_blueprint(api_bp)
```

## 10) Isolate Deprecated API Usage

**Problema**: API obsoleta (ex.: `Query.get` no SQLAlchemy legado).

```python
# Before
user = User.query.get(user_id)
```

```python
# After
user = db.session.get(User, user_id)
```

