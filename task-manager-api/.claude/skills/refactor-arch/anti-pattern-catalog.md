# Anti-Pattern Catalog

- Hardcoded credentials/secrets (`CRITICAL`)
- SQL injection por concatenação (`CRITICAL`)
- God class/god module (`CRITICAL`)
- Endpoint sensível sem auth (`HIGH`)
- Lógica de negócio em routes/controllers (`HIGH`)
- Estado global mutável (`HIGH`)
- Hash fraco de senha (`HIGH`)
- N+1 queries (`MEDIUM`)
- Duplicação de lógica (`MEDIUM`)
- API deprecated (`MEDIUM`)
- Magic numbers (`LOW`)
- Imports/deps não usados (`LOW`)

Cada finding deve ter arquivo + linhas exatas.

