# Refactoring Playbook

Padrões obrigatórios:

1. Extrair config hardcoded para env/config module.
2. Trocar SQL concatenado por query parametrizada.
3. Dividir God class em routes/controllers/services/repositories.
4. Extrair regras de negócio de rotas para services.
5. Introduzir middleware de erro centralizado.
6. Substituir hash fraco por algoritmo seguro.
7. Resolver N+1 com JOIN/eager loading.
8. Remover estado global mutável e usar injeção/factory.
9. Consolidar registro de rotas em módulo de views.
10. Migrar APIs deprecated para equivalentes suportados.

