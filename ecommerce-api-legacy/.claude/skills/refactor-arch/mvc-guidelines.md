# MVC Guidelines

- **Model**: dados e regras de domínio coesas.
- **Views/Routes**: mapeamento de endpoint e contrato HTTP.
- **Controllers**: orquestração de requisições e respostas.
- **Services**: regras de negócio reutilizáveis.
- **Repositories**: acesso a dados isolado.
- **Middlewares**: auth, autorização e tratamento de erros.

Critérios:

- Config centralizada (sem segredo hardcoded).
- Controllers finos.
- Sem SQL inline em rota.
- Entrypoint claro.
- Endpoints originais preservados.

