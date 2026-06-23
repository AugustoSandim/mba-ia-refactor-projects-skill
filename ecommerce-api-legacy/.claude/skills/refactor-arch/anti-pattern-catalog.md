# Anti-Pattern Catalog

Mínimo de anti-patterns para auditoria:

1. Hardcoded credentials/secrets (`CRITICAL`)
2. SQL injection por concatenação (`CRITICAL`)
3. God class/god module (`CRITICAL`)
4. Endpoint sensível sem auth (`HIGH`)
5. Lógica de negócio em rota/controller (`HIGH`)
6. Estado global mutável (`HIGH`)
7. Hash fraco de senha (`HIGH`)
8. N+1 queries (`MEDIUM`)
9. Lógica duplicada (`MEDIUM`)
10. Uso de API deprecated (`MEDIUM`)
11. Magic numbers (`LOW`)
12. Imports/dependências não usados (`LOW`)

Cada finding deve trazer: severidade, arquivo:linhas, descrição, impacto e recomendação.

