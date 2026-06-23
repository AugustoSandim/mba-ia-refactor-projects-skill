# Anti-Pattern Catalog

Catálogo base para auditoria arquitetural orientada a MVC/SOLID.

## Convenção de severidade

- `CRITICAL`: risco grave de segurança/arquitetura.
- `HIGH`: forte quebra de separação de responsabilidades/manutenibilidade.
- `MEDIUM`: impacto moderado de performance/qualidade/padronização.
- `LOW`: legibilidade e higiene técnica.

## Anti-patterns

### 1) Hardcoded Credentials or Secrets

- **Severity**: `CRITICAL`
- **Sinais**:
  - `SECRET_KEY = "..."`, chaves de gateway, senhas SMTP no código.
- **Impacto**: vazamento de segredos e comprometimento de segurança.
- **Recomendação**: mover para variáveis de ambiente + módulo de config.

### 2) SQL Injection by String Concatenation

- **Severity**: `CRITICAL`
- **Sinais**:
  - SQL montado com concatenação/interpolação de entrada de usuário.
- **Impacto**: execução arbitrária de SQL.
- **Recomendação**: consultas parametrizadas (`?`, `$1`, ORM filters).

### 3) God Class / God Module

- **Severity**: `CRITICAL`
- **Sinais**:
  - arquivo/classe concentra rotas, regras de negócio e acesso a dados.
- **Impacto**: alta fragilidade, baixa testabilidade e acoplamento extremo.
- **Recomendação**: separar em controllers/services/repositories/models.

### 4) Missing Auth on Sensitive Endpoints

- **Severity**: `HIGH`
- **Sinais**:
  - endpoints administrativos ou dados sensíveis sem autenticação/autorização.
- **Impacto**: acesso indevido a dados e operações críticas.
- **Recomendação**: middleware auth + regras de autorização por papel.

### 5) Business Rules in Routes/Controllers

- **Severity**: `HIGH`
- **Sinais**:
  - validações complexas, transações e regras de domínio dentro de rota HTTP.
- **Impacto**: quebra de SRP, testes difíceis, alta duplicação.
- **Recomendação**: mover regras para services/use-cases.

### 6) Global Mutable State

- **Severity**: `HIGH`
- **Sinais**:
  - singletons globais mutáveis (`globalCache`, conexão global sem factory).
- **Impacto**: efeitos colaterais, concorrência problemática, baixa previsibilidade.
- **Recomendação**: injeção de dependência e factories explícitas.

### 7) N+1 Query Pattern

- **Severity**: `MEDIUM`
- **Sinais**:
  - loop de entidades com query adicional por item.
- **Impacto**: degradação de performance conforme volume cresce.
- **Recomendação**: JOIN/eager loading/agregações.

### 8) Duplicated Business Logic

- **Severity**: `MEDIUM`
- **Sinais**:
  - blocos similares repetidos em múltiplos endpoints/módulos.
- **Impacto**: divergência e manutenção custosa.
- **Recomendação**: extrair função/service compartilhado.

### 9) Weak Password Hashing

- **Severity**: `HIGH`
- **Sinais**:
  - MD5/SHA1 custom para senha.
- **Impacto**: proteção insuficiente de credenciais.
- **Recomendação**: `bcrypt`, `argon2` ou equivalente seguro.

### 10) Deprecated APIs

- **Severity**: `MEDIUM`
- **Sinais**:
  - Python: `Query.get(...)` em SQLAlchemy legado.
  - Node: APIs marcadas como deprecated em docs oficiais.
- **Impacto**: risco de quebra em upgrades e dívida técnica.
- **Recomendação**:
  - SQLAlchemy: preferir `db.session.get(Model, id)` no 2.x.
  - Node: migrar para equivalente suportado.

### 11) Magic Numbers / Opaque Constants

- **Severity**: `LOW`
- **Sinais**:
  - limites e multiplicadores sem nome/contexto.
- **Impacto**: reduz clareza e dificulta ajuste de regras.
- **Recomendação**: extrair constantes nomeadas/config.

### 12) Unused Imports/Dependencies

- **Severity**: `LOW`
- **Sinais**:
  - imports/dependências nunca usados.
- **Impacto**: ruído, dívida técnica e confusão arquitetural.
- **Recomendação**: remover ou integrar de forma explícita.

