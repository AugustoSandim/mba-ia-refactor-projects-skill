# refactor-arch

Skill agnóstica para auditoria e refatoração arquitetural MVC.

## Fases obrigatórias

1. **Phase 1 - Analysis**: detectar stack/domínio/arquitetura e imprimir resumo.
2. **Phase 2 - Audit**: mapear anti-patterns, classificar severidade, gerar relatório e pausar para confirmação.
3. **Phase 3 - Refactor**: aplicar refatoração MVC, corrigir achados prioritários e validar boot/endpoints.

## Referências

- `project-analysis-heuristics.md`
- `anti-pattern-catalog.md`
- `audit-report-template.md`
- `mvc-guidelines.md`
- `refactoring-playbook.md`

## Gate obrigatório da Fase 2

Após gerar o relatório, interromper e perguntar:

```text
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

Sem confirmação explícita, não modificar arquivos.

