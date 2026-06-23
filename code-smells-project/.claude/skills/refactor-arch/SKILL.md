# refactor-arch

Skill para auditoria arquitetural e refatoração MVC agnóstica de tecnologia.

## Objetivo

Executar uma jornada em 3 fases:

1. **Phase 1 - Analysis**: detectar stack, arquitetura atual e domínio.
2. **Phase 2 - Audit**: identificar anti-patterns, classificar severidade, gerar relatório estruturado e pausar para confirmação humana.
3. **Phase 3 - Refactor**: aplicar refatoração para MVC, corrigir achados prioritários e validar funcionamento.

## Entradas esperadas

- Diretório do projeto alvo.
- Código-fonte local do backend (Python/Flask, Node/Express ou equivalente).

## Referências obrigatórias

Leia e siga sempre:

- `project-analysis-heuristics.md`
- `anti-pattern-catalog.md`
- `audit-report-template.md`
- `mvc-guidelines.md`
- `refactoring-playbook.md`

## Processo obrigatório

### PHASE 1: PROJECT ANALYSIS

1. Detectar linguagem e framework por heurísticas:
   - Dependências, imports/requires, estrutura de arquivos e entrypoint.
2. Inferir arquitetura atual:
   - Monolítica, parcialmente organizada, pseudo-MVC etc.
3. Identificar domínio da aplicação:
   - Entidades e fluxos principais (ex.: usuários, pedidos, tarefas).
4. Produzir resumo objetivo:
   - Language, Framework, Dependencies, Domain, Architecture, Source files, DB objects.

Formato mínimo:

```text
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:
Framework:
Dependencies:
Domain:
Architecture:
Source files:
DB tables/collections:
================================
```

### PHASE 2: ARCHITECTURE AUDIT

1. Cruzar código com o catálogo de anti-patterns.
2. Gerar findings com:
   - Severidade (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
   - Arquivo e linhas exatas
   - Descrição, impacto e recomendação
3. Ordenar findings por severidade (CRITICAL -> LOW).
4. Garantir no mínimo:
   - 5 findings totais
   - pelo menos 1 finding `CRITICAL` ou `HIGH`
5. Incluir checagem de APIs deprecated (quando aplicável).
6. Gerar relatório no formato de `audit-report-template.md`.
7. **Pausar obrigatoriamente** e solicitar confirmação antes de qualquer modificação:

```text
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

Se a resposta for `n`, encerrar após salvar o relatório.

### PHASE 3: MVC REFACTOR + VALIDATION

1. Planejar transformação com base em `mvc-guidelines.md` e `refactoring-playbook.md`.
2. Aplicar refatoração incremental:
   - Extrair configuração hardcoded para módulo de config.
   - Separar responsabilidades em Models, Views/Routes, Controllers.
   - Introduzir camada de serviços/repositórios quando necessário para reduzir acoplamento.
   - Centralizar tratamento de erros.
3. Preservar endpoints/contratos existentes para evitar regressão funcional.
4. Validar resultado:
   - Aplicação inicia sem erro.
   - Endpoints principais respondem.
   - Achados críticos e high eliminados ou mitigados.
5. Emitir resumo final:

```text
================================
PHASE 3: REFACTORING COMPLETE
================================
New Project Structure:
...

Validation:
  ✓ Application boots without errors
  ✓ Core endpoints respond correctly
  ✓ Critical findings addressed
================================
```

## Regras de qualidade

- Ser objetivo e técnico, sem linguagem vaga.
- Preferir mudanças pequenas e verificáveis.
- Não remover funcionalidades do domínio original.
- Não alterar contratos de API sem necessidade.
- Quando houver trade-off, priorizar segurança e separação de responsabilidades.

