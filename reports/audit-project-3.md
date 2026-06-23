================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask + SQLAlchemy
Files:   13 analyzed | ~1100 lines

Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 3 | LOW: 3

Findings

[CRITICAL] Secret key hardcoded
File: task-manager-api/app.py:13
Description: `SECRET_KEY` definido diretamente no código.
Impact: Risco de exposição de segredo em ambientes compartilhados.
Recommendation: Mover para variável de ambiente.

[CRITICAL] Exposição de hash de senha em respostas
File: task-manager-api/models/user.py:16-25
Description: Método `to_dict()` retornava campo `password`.
Impact: Divulgação de credencial derivada.
Recommendation: Remover campo sensível de serialização.

[HIGH] Hash de senha fraco (MD5)
File: task-manager-api/models/user.py:27-32
Description: Senhas processadas com MD5.
Impact: Vulnerável a cracking.
Recommendation: Adotar hash moderno (`pbkdf2/bcrypt/argon2`).

[HIGH] Rotas com lógica de negócio acoplada
File: task-manager-api/routes/task_routes.py:11-299
Description: Regras de validação, transformação e persistência no layer de rota.
Impact: Violação de separação MVC e baixa testabilidade.
Recommendation: Extrair para controllers/services.

[HIGH] Endpoint de login sem autenticação real
File: task-manager-api/routes/user_routes.py:185-211
Description: Retorno de token fake sem middleware de autorização para demais rotas.
Impact: Inconsistência de segurança.
Recommendation: Introduzir middleware/token real ou explicitar escopo local.

[MEDIUM] N+1 query em listagem de tasks
File: task-manager-api/routes/task_routes.py:41-57
Description: Busca usuário e categoria por tarefa em loop.
Impact: Custo de consulta cresce linearmente.
Recommendation: Usar eager loading/join.

[MEDIUM] APIs deprecated (`Query.get`)
File: task-manager-api/routes/task_routes.py:67,117,122
Description: Uso de `Model.query.get(...)` em SQLAlchemy 2.x.
Impact: Dívida técnica e risco de quebra futura.
Recommendation: Migrar para `db.session.get(Model, id)`.

[MEDIUM] Categorias misturadas em report routes
File: task-manager-api/routes/report_routes.py:157-223
Description: CRUD de categoria implementado no módulo de relatórios.
Impact: Responsabilidades cruzadas.
Recommendation: Extrair para rota/controlador dedicado de categoria.

[LOW] Imports não utilizados
File: task-manager-api/app.py:7
Description: `sys` e `json` sem uso.
Impact: Ruído de manutenção.
Recommendation: Limpar imports.

[LOW] Prints operacionais em vez de logging estruturado
File: task-manager-api/routes/task_routes.py:149,219,234
Description: Mensagens operacionais emitidas com `print`.
Impact: Observabilidade limitada.
Recommendation: Padronizar logger.

[LOW] Dependências sem uso efetivo
File: task-manager-api/requirements.txt:4-6
Description: `marshmallow`, `requests` e `python-dotenv` sem integração consistente no fluxo original.
Impact: Complexidade desnecessária.
Recommendation: Remover ou integrar corretamente.

================================
Total: 11 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y

