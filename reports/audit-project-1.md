================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines

Summary
CRITICAL: 3 | HIGH: 3 | MEDIUM: 3 | LOW: 2

Findings

[CRITICAL] SQL Injection via string concatenation
File: code-smells-project/models.py:47-50
Description: SQL de inserção de produto é montado por concatenação de strings com entrada externa.
Impact: Permite manipulação de consulta e comprometimento de dados.
Recommendation: Substituir por query parametrizada.

[CRITICAL] Hardcoded secret key
File: code-smells-project/app.py:7
Description: `SECRET_KEY` fixo no código-fonte.
Impact: Exposição de segredo e risco de comprometimento de sessão.
Recommendation: Extrair para variável de ambiente e módulo de configuração.

[CRITICAL] God module com responsabilidades de dados e negócio
File: code-smells-project/models.py:1-315
Description: Um único módulo concentra produtos, usuários, pedidos, relatório e queries SQL.
Impact: Alto acoplamento e baixa testabilidade.
Recommendation: Separar em repositories/services/controllers.

[HIGH] Endpoint administrativo sem proteção
File: code-smells-project/app.py:47-78
Description: Endpoints `/admin/reset-db` e `/admin/query` expõem operações críticas sem controle.
Impact: Risco de perda/extração de dados.
Recommendation: Proteger com token/middleware e restringir consultas.

[HIGH] Senhas em texto puro no banco
File: code-smells-project/database.py:76-79
Description: Usuários seedados com senha sem hash.
Impact: Vazamento de credenciais em caso de acesso indevido.
Recommendation: Aplicar hash seguro (`pbkdf2/bcrypt/argon2`).

[HIGH] Health endpoint expõe informações sensíveis
File: code-smells-project/controllers.py:285-289
Description: Retorna `debug`, `db_path` e `secret_key` em resposta pública.
Impact: Facilita reconhecimento e exploração.
Recommendation: Limitar payload do health a status operacional.

[MEDIUM] N+1 queries ao listar pedidos
File: code-smells-project/models.py:171-232
Description: Para cada pedido, busca itens e produto em loops aninhados.
Impact: Degradação de performance com aumento de volume.
Recommendation: Consolidar consulta com JOIN.

[MEDIUM] Duplicação de lógica em listagem de pedidos
File: code-smells-project/models.py:171-200,203-232
Description: Fluxo quase idêntico entre listagem por usuário e listagem geral.
Impact: Maior custo de manutenção e risco de divergência.
Recommendation: Extrair função reutilizável.

[MEDIUM] Falta de transação explícita no fluxo de criação de pedido
File: code-smells-project/models.py:133-169
Description: Sequência de validações e inserts sem rollback explícito para falhas intermediárias.
Impact: Possibilidade de estado inconsistente.
Recommendation: Delimitar transação de ponta a ponta.

[LOW] Magic numbers em regra de desconto
File: code-smells-project/models.py:257-262
Description: Limiares e percentuais de desconto hardcoded sem constantes nomeadas.
Impact: Dificulta governança e ajuste de regra.
Recommendation: Externalizar para configuração.

[LOW] Logging ad-hoc com print
File: code-smells-project/controllers.py:8,57,208-210
Description: Uso de `print` para logs operacionais e notificação.
Impact: Observabilidade inconsistente.
Recommendation: Padronizar logger estruturado.

================================
Total: 11 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y

