# Project Analysis Heuristics

- Detectar stack por dependências/imports (`requirements.txt`, `package.json`, `flask`, `express`).
- Detectar persistência por sinais de ORM/SQL raw (`SQLAlchemy`, `sqlite3`, queries inline).
- Detectar domínio por rotas, entidades e tabelas.
- Classificar arquitetura atual: monolítica, pseudo-camadas ou MVC parcial.

Resumo mínimo da Fase 1:

- Language
- Framework
- Dependencies
- Domain
- Architecture
- Source files analyzed
- DB tables/collections

