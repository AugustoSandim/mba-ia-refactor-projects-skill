================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express
Files:   3 analyzed | ~150 lines

Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 3 | LOW: 2

Findings

[CRITICAL] Hardcoded credentials in utility module
File: ecommerce-api-legacy/src/utils.js:1-7
Description: Configuração contém credenciais e chave de gateway fixas no código.
Impact: Exposição de segredos.
Recommendation: Usar variáveis de ambiente.

[CRITICAL] God class centralizando DB, rotas e negócio
File: ecommerce-api-legacy/src/AppManager.js:4-139
Description: Classe única concentra inicialização, SQL, rotas e fluxo de checkout.
Impact: Forte acoplamento e baixa testabilidade.
Recommendation: Separar em controllers/services/repositories.

[HIGH] Lógica de pagamento dentro da rota de checkout
File: ecommerce-api-legacy/src/AppManager.js:43-63
Description: Regra de negócio e persistência diretamente no handler HTTP.
Impact: Dificulta evolução e testes unitários.
Recommendation: Extrair para service.

[HIGH] Endpoint administrativo sem autenticação
File: ecommerce-api-legacy/src/AppManager.js:80-129
Description: Relatório financeiro acessível sem mecanismo de auth/autorização.
Impact: Exposição de dados de receita e alunos.
Recommendation: Aplicar middleware de autenticação/autorização.

[HIGH] Hash de senha não criptograficamente seguro
File: ecommerce-api-legacy/src/utils.js:17-23
Description: Função `badCrypto` usa concatenação base64 em loop.
Impact: Proteção inadequada de senha.
Recommendation: Substituir por hash robusto.

[MEDIUM] N+1 queries no relatório financeiro
File: ecommerce-api-legacy/src/AppManager.js:89-127
Description: Loop em cursos e matrículas executa consultas adicionais por aluno/pagamento.
Impact: Performance piora com crescimento de dados.
Recommendation: Reduzir round-trips e consolidar acesso em repository/service.

[MEDIUM] Deleção de usuário deixa dados órfãos
File: ecommerce-api-legacy/src/AppManager.js:131-137
Description: Remove usuário sem tratar matrículas e pagamentos relacionados.
Impact: Inconsistência de dados.
Recommendation: Aplicar estratégia transacional/cascade.

[MEDIUM] API deprecated no ecossistema ORM/consulta não tratada
File: ecommerce-api-legacy/src/AppManager.js:89-127
Description: Padrão de callbacks aninhados legado sem isolamento de acesso moderno.
Impact: Dificulta manutenção e migração de stack.
Recommendation: Adotar camada de repository/service com async/await.

[LOW] Nomes crípticos no payload de checkout
File: ecommerce-api-legacy/src/AppManager.js:29-33
Description: Campos `usr`, `eml`, `c_id` e `card` reduzem legibilidade.
Impact: Curva de manutenção maior.
Recommendation: Padronizar nomenclatura interna sem quebrar contrato externo.

[LOW] Import não utilizado
File: ecommerce-api-legacy/src/AppManager.js:2
Description: `totalRevenue` importado mas não utilizado.
Impact: Ruído técnico.
Recommendation: Remover código morto.

================================
Total: 10 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y

