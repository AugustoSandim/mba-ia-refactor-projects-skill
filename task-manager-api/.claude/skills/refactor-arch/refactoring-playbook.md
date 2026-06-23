# Refactoring Playbook

Transformações mandatórias:

1. Extrair segredos hardcoded para configuração.
2. Parametrizar queries SQL.
3. Dividir God module/class em camadas MVC.
4. Extrair regra de negócio de rotas para controllers/services.
5. Adotar tratamento centralizado de erros.
6. Substituir hash fraco de senha por algoritmo seguro.
7. Eliminar N+1 com JOIN/eager loading.
8. Remover estado global mutável e usar factories.
9. Centralizar roteamento em módulo de views.
10. Substituir APIs deprecated por alternativas modernas.

