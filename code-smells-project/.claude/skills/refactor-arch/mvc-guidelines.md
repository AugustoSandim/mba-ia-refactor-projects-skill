# MVC Guidelines

## Objetivo arquitetural

Estabelecer separação clara entre:

- **Model**: representação de dados + regras de domínio essenciais.
- **View/Routes**: interface HTTP (mapeamento de endpoint, parsing, status code).
- **Controller**: orquestra fluxo da requisição e chama serviços/repositórios.

## Responsabilidades por camada

### Models

- Entidades e contratos de dados.
- Regras de domínio coesas (ex.: validação de status da task).
- Não devem conhecer detalhes de transporte HTTP.

### Views/Routes

- Definem rotas e método HTTP.
- Delegam para controllers.
- Não implementam regra de negócio complexa.

### Controllers

- Recebem input da rota e coordenam caso de uso.
- Chamam services/repositories.
- Montam resposta HTTP final.

### Services (suporte recomendado)

- Regras de negócio reutilizáveis.
- Transações e fluxos multi-entidade.

### Repositories (suporte recomendado)

- Acesso a dados isolado.
- Query parametrizada/ORM.

### Middlewares

- Cross-cutting concerns: autenticação, autorização, tratamento de erro.

## Regras de design

- Entry point único e claro (composition root).
- Configuração centralizada (`config/settings` ou equivalente).
- Erros tratados em um ponto central.
- Sem segredos hardcoded.
- Sem SQL inline em rotas/controllers.
- Controllers finos; services concentram lógica.

## Definição de pronto (DoD) para refatoração

- Estrutura do projeto reflete MVC explicitamente.
- Endpoints originais continuam respondendo.
- Achados CRITICAL/HIGH do relatório foram corrigidos ou mitigados.
- Aplicação inicializa sem exceções.

