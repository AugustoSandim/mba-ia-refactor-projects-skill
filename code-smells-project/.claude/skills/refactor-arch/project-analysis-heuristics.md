# Project Analysis Heuristics

## Objetivo

Detectar stack, arquitetura e domínio de forma consistente em diferentes tecnologias.

## Heurísticas de detecção de linguagem/framework

### Python

Sinais:

- `requirements.txt`, `pyproject.toml`
- `from flask import ...`, `from fastapi import ...`, `django.*`

Inferência:

- `Flask` quando há `flask` em dependências/imports.
- `Flask + SQLAlchemy` quando houver `flask_sqlalchemy` ou modelos com ORM.

### Node.js

Sinais:

- `package.json`
- `const express = require("express")` ou `import express from "express"`

Inferência:

- `Express` quando houver dependência/import de `express`.

## Heurísticas de banco de dados

- SQLite: `sqlite3`, `sqlite:///...`, `new sqlite3.Database(...)`
- SQLAlchemy ORM: modelos com `db.Model`, `db.Column`
- SQL raw: presença massiva de `SELECT/INSERT/UPDATE/DELETE` inline

## Heurísticas de arquitetura atual

- **Monolítica**: poucas classes/arquivos concentrando rotas + regras + SQL.
- **Pseudo-camadas**: pastas separadas existem, mas rotas ainda têm lógica de negócio.
- **MVC parcial**: camadas existem, porém com vazamentos de responsabilidade.

## Heurísticas de domínio

Identificar entidades de negócio por:

- nomes de tabelas/modelos (`users`, `tasks`, `orders`, `products`)
- rotas (`/pedidos`, `/tasks`, `/checkout`)
- nomes de serviços/controladores

## Métricas mínimas do resumo da fase 1

- Linguagem
- Framework
- Dependências principais
- Domínio inferido
- Arquitetura atual
- Quantidade de arquivos analisados
- Objetos de persistência (tabelas/coleções)

## Red flags de arquitetura (atalhos para fase 2)

- Classe com >200 linhas e múltiplas responsabilidades.
- SQL inline dentro de rota/controller.
- Segredos hardcoded.
- Sem camada de erro centralizada.
- Sem fronteira clara entre HTTP e regras de negócio.

