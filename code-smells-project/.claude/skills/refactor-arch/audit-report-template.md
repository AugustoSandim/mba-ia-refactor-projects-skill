# Audit Report Template

Use este formato na saída da Fase 2.

```markdown
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <project-name>
Stack:   <language + framework>
Files:   <count> analyzed | ~<loc> lines

Summary
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>

Findings

[<SEVERITY>] <Title>
File: <path>:<start>-<end>
Description: <objective description>
Impact: <objective impact>
Recommendation: <actionable recommendation>

[<SEVERITY>] <Title>
File: <path>:<start>-<end>
Description: ...
Impact: ...
Recommendation: ...

================================
Total: <n> findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

## Regras obrigatórias do relatório

- Ordenar findings por severidade (`CRITICAL` -> `LOW`).
- Informar arquivo e linhas exatas de cada finding.
- Linguagem objetiva, sem termos vagos.
- Recomendações acionáveis e alinhadas ao padrão MVC.
- Registrar explicitamente a pausa de confirmação antes da Fase 3.

