# MVC Guidelines

- Models: dados e regras de domínio.
- Views/Routes: roteamento e contrato HTTP.
- Controllers: orquestração de caso de uso.
- Services: regras de negócio reutilizáveis.
- Repositories: acesso a dados.
- Middlewares: auth e erro.

Qualidade mínima:

- Segredos em config/env.
- Controllers finos.
- Sem lógica de negócio pesada em rotas.
- Entrypoint claro.
- Endpoints preservados após refatoração.

