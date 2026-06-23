# Skill de Auditoria e Refatoração Arquitetural (MVC)

Este repositório contém a implementação completa do desafio:

- criação da skill `refactor-arch`;
- execução em 3 projetos legados;
- geração de 3 relatórios de auditoria;
- refatoração arquitetural para MVC sem quebrar os endpoints principais.

## Estrutura final

```text
mba-ia-refactor-projects-skill/
├── README.md
├── reports/
│   ├── audit-project-1.md
│   ├── audit-project-2.md
│   └── audit-project-3.md
├── code-smells-project/
│   └── .claude/skills/refactor-arch/
├── ecommerce-api-legacy/
│   └── .claude/skills/refactor-arch/
└── task-manager-api/
    └── .claude/skills/refactor-arch/
```

## A) Análise Manual

### Projeto 1 - `code-smells-project` (Python/Flask)

1. **CRITICAL** - SQL injection por concatenação de string em queries (`models.py`).
   - Relevância: risco direto de comprometimento de dados.
2. **HIGH** - Endpoints administrativos sem proteção (`app.py`).
   - Relevância: permite operações destrutivas sem controle.
3. **MEDIUM** - N+1 queries na listagem de pedidos (`models.py`).
   - Relevância: degrada performance conforme volume cresce.
4. **MEDIUM** - Duplicação da lógica de listagem de pedidos (`models.py`).
   - Relevância: manutenção cara e propensa a divergência.
5. **LOW** - Magic numbers em regra de desconto (`models.py`).
   - Relevância: baixa clareza para manutenção.
6. **LOW** - Logging ad-hoc com `print` (`controllers.py`).
   - Relevância: observabilidade inconsistente.

### Projeto 2 - `ecommerce-api-legacy` (Node.js/Express)

1. **CRITICAL** - Hardcoded credentials e chaves (`src/utils.js` original).
   - Relevância: exposição de segredos.
2. **HIGH** - Lógica de negócio pesada no handler de checkout (`src/AppManager.js` original).
   - Relevância: viola SRP e dificulta testes.
3. **MEDIUM** - N+1 queries no relatório financeiro (`src/AppManager.js` original).
   - Relevância: ineficiência de consulta.
4. **MEDIUM** - Deleção de usuário com dados órfãos (`src/AppManager.js` original).
   - Relevância: inconsistência de dados.
5. **LOW** - Nomes de payload crípticos (`usr`, `eml`, `c_id`) no checkout.
   - Relevância: reduz legibilidade.
6. **LOW** - Import não utilizado (`totalRevenue`) no legado.
   - Relevância: ruído técnico.

### Projeto 3 - `task-manager-api` (Python/Flask)

1. **CRITICAL** - `SECRET_KEY` hardcoded (`app.py` original).
   - Relevância: risco de segurança.
2. **HIGH** - Hash de senha com MD5 (`models/user.py` original).
   - Relevância: algoritmo inseguro.
3. **MEDIUM** - N+1 na listagem de tasks (`routes/task_routes.py` original).
   - Relevância: queda de performance.
4. **MEDIUM** - Uso de API deprecated (`Query.get`) em várias rotas.
   - Relevância: dívida técnica de compatibilidade.
5. **LOW** - Imports não utilizados (`app.py`, rotas).
   - Relevância: piora legibilidade e manutenção.
6. **LOW** - Uso de `print` no fluxo de API.
   - Relevância: logging não padronizado.

## B) Construção da Skill

### Decisões de design

- Skill criada com nome fixo `refactor-arch` em `.claude/skills/refactor-arch/`.
- Orquestração em 3 fases sequenciais:
  - **Fase 1**: detecção de stack e arquitetura;
  - **Fase 2**: auditoria com severidade e template padronizado;
  - **Fase 3**: refatoração MVC + validação.
- Pausa obrigatória entre fase 2 e 3 com confirmação explícita (`[y/n]`).

### Arquivos de referência incluídos

- `SKILL.md`
- `project-analysis-heuristics.md`
- `anti-pattern-catalog.md`
- `audit-report-template.md`
- `mvc-guidelines.md`
- `refactoring-playbook.md`

### Catálogo de anti-patterns

O catálogo contempla no mínimo 8 anti-patterns, com distribuição entre:

- `CRITICAL`: hardcoded secrets, SQL injection, god class/module;
- `HIGH`: ausência de auth em rotas sensíveis, regra de negócio em rota, hash fraco;
- `MEDIUM`: N+1, duplicação de lógica, API deprecated;
- `LOW`: magic numbers, imports/deps não usados.

### Playbook de transformação

O playbook contém 10 padrões de transformação, incluindo:

- extração de configuração;
- parametrização de SQL;
- separação em MVC;
- extração de regras para services/controllers;
- tratamento centralizado de erros;
- atualização de APIs deprecated.

### Como a skill foi mantida agnóstica de tecnologia

- heurísticas por sinais de arquivo/dependência/import em vez de nomes hardcoded de projeto;
- guidelines de arquitetura orientadas a responsabilidades (não a framework específico);
- playbook com exemplos em Python e JavaScript.

### Principais desafios e solução

- **Ambientes distintos (Flask e Express)**: resolvido com detecção por heurística e padrões comuns de camada.
- **Compatibilidade funcional**: preservação explícita dos endpoints originais e smoke tests após refatoração.
- **Legado parcialmente organizado**: extração de controllers sem quebra de contratos.

## C) Resultados

### Resumo dos relatórios

- `reports/audit-project-1.md`: 11 findings (3 CRITICAL, 3 HIGH, 3 MEDIUM, 2 LOW).
- `reports/audit-project-2.md`: 10 findings (2 CRITICAL, 3 HIGH, 3 MEDIUM, 2 LOW).
- `reports/audit-project-3.md`: 11 findings (2 CRITICAL, 3 HIGH, 3 MEDIUM, 3 LOW).

### Comparação antes/depois

#### Projeto 1 - `code-smells-project`

- **Antes**: `app.py`, `controllers.py`, `models.py`, `database.py` acoplados.
- **Depois**: `src/config`, `src/database`, `src/repositories`, `src/services`, `src/controllers`, `src/views`, `src/middlewares`.

#### Projeto 2 - `ecommerce-api-legacy`

- **Antes**: `AppManager` concentrava rotas + SQL + negócio.
- **Depois**: `config`, `database`, `repositories`, `services`, `controllers`, `views`, `middlewares`.

#### Projeto 3 - `task-manager-api`

- **Antes**: rotas com lógica pesada e categorias misturadas com relatórios.
- **Depois**: camada `controllers/` dedicada e `routes/category_routes.py` separada.

### Logs de validação (execução local)

#### Projeto 1

```text
GET / -> 200
GET /health -> 200
GET /produtos -> 200
GET /usuarios -> 200
POST /login -> 200
GET /relatorios/vendas -> 200
```

#### Projeto 2

```text
checkout_ok:200
report:200
delete:200
```

#### Projeto 3

```text
GET / -> 200
GET /health -> 200
GET /tasks -> 200
GET /users -> 200
POST /login -> 200
GET /reports/summary -> 200
GET /categories -> 200
```

### Checklist de validação

#### Projeto 1 - code-smells-project

- [x] Linguagem detectada corretamente
- [x] Framework detectado corretamente
- [x] Domínio descrito corretamente
- [x] Relatório com findings ordenados por severidade
- [x] Pausa entre Fase 2 e Fase 3
- [x] Estrutura MVC criada
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem

#### Projeto 2 - ecommerce-api-legacy

- [x] Linguagem detectada corretamente
- [x] Framework detectado corretamente
- [x] Relatório com >= 5 findings
- [x] Inclusão de finding CRITICAL/HIGH
- [x] Pausa entre Fase 2 e Fase 3
- [x] Estrutura MVC criada
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem

#### Projeto 3 - task-manager-api

- [x] Linguagem detectada corretamente
- [x] Framework detectado corretamente
- [x] Relatório com >= 5 findings
- [x] Inclusão de finding CRITICAL/HIGH
- [x] Pausa entre Fase 2 e Fase 3
- [x] Extração de controllers
- [x] Error handling funcional
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem

## D) Como Executar

### Pré-requisitos

- Python 3.9+
- Node.js 18+
- Dependências instaladas por projeto (`pip`/`npm`)
- Ferramenta com suporte a skills (convenção usada: `Claude-style`)

### 1) Projeto 1 - `code-smells-project`

```bash
cd code-smells-project
python3 -m pip install -r requirements.txt
python3 app.py
```

### 2) Projeto 2 - `ecommerce-api-legacy`

```bash
cd ecommerce-api-legacy
npm install
npm start
```

### 3) Projeto 3 - `task-manager-api`

```bash
cd task-manager-api
python3 -m pip install -r requirements.txt
python3 seed.py
python3 app.py
```

### Invocação da skill

```bash
claude "/refactor-arch"
```

### Como validar que funcionou

- conferir relatório da fase 2 salvo em `reports/audit-project-{1,2,3}.md`;
- confirmar pausa antes da fase 3 (`Proceed with refactoring? [y/n]`);
- validar boot da API;
- executar smoke dos endpoints principais.

