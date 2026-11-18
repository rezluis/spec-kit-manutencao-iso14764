---
description: "Consulta e filtra issues do GitHub por labels, datas, estado e outros critérios"
---

# Comando: Consulta de Issues

Este comando permite consultar e filtrar issues de um repositório GitHub de forma estruturada.

## Entrada do Usuário
$ARGUMENTS

## Instruções para o Agente

Você deve executar o seguinte fluxo de trabalho:

1.  **Extrair os Parâmetros:** Da entrada fornecida em `$ARGUMENTS`, extraia:
    - `owner` e `repo` (do formato `owner/repo` ou da URL completa do repositório)
    - Filtros opcionais:
      - `state` (`open`, `closed`, `all`)
      - `labels` (lista de labels, ex: `bug`, `enhancement`)
      - `created_after` e `created_before` (formato `YYYY-MM-DD`)
      - `updated_after` (formato `YYYY-MM-DD`)
      - `text_search` (texto livre para buscar no título/corpo)
      - `author` (username do autor)
      - `assignee` (username do responsável)
      - `limit` (número máximo de resultados, padrão: 30)

2.  **Invocar a Skill de Consulta:** Use a skill `issue-query` para executar a busca:

call skill issue-query
owner={owner}
repo={repo}
filters={filters}
limit={limit}


3.  **Apresentar os Resultados:** Formate os resultados em uma tabela legível:
| # | Título | Estado | Labels | Criado em | Autor |
|---|--------|--------|--------|-----------|-------|
| 42 | Erro 500 no login | open | bug, triage | 2025-01-15 | rezluis |

4.  **Resumo:** Apresente um resumo com:
- Total de issues encontradas
- Distribuição por estado (abertas/fechadas)
- Distribuição por labels mais frequentes

5.  **Finalizar:** Pergunte ao usuário se ele deseja:
- Ver os detalhes de alguma issue específica
- Executar `/speckit.maintenance.analyze` em alguma issue listada
- Refinar a busca com novos filtros

## Exemplos de Uso

- `/speckit.maintenance.issues rezluis/todo-app`
→ Lista todas as issues abertas

- `/speckit.maintenance.issues rezluis/todo-app state=closed label=bug`
→ Lista bugs fechados

- `/speckit.maintenance.issues rezluis/todo-app created_after=2025-01-01 created_before=2025-01-31`
→ Lista issues criadas em janeiro de 2025

- `/speckit.maintenance.issues rezluis/todo-app label=enhancement state=open`
→ Lista melhorias abertas

- `/speckit.maintenance.issues rezluis/todo-app text_search="login"`
→ Busca issues que contenham "login" no título ou corpo


