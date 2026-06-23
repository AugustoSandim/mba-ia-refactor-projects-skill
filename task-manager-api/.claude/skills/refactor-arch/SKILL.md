# refactor-arch

Skill agnóstica para análise, auditoria e refatoração MVC.

## Sequência mandatória

1. **Phase 1 - Analysis**: detectar linguagem/framework/domínio/arquitetura.
2. **Phase 2 - Audit**: identificar anti-patterns com severidade e relatório estruturado.
3. **Phase 3 - Refactor**: aplicar MVC e validar aplicação.

## Arquivos de referência

- `project-analysis-heuristics.md`
- `anti-pattern-catalog.md`
- `audit-report-template.md`
- `mvc-guidelines.md`
- `refactoring-playbook.md`

## Regra crítica

Após Fase 2, pausar e solicitar confirmação:

```text
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

Somente seguir para Fase 3 após confirmação explícita.

