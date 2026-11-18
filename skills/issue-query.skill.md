---
description: "Consulta issues do GitHub com filtros por label, data, estado e campos"
mcp_servers: ["github"]
---

## Propósito
Esta skill permite consultar issues do GitHub de forma estruturada, aplicando filtros por labels, datas, estado, e campos presentes na descrição.

## Entrada

```json
{
  "owner": "string",
  "repo": "string",
  "filters": {
    "state": "open|closed|all",
    "labels": ["string"],
    "created_after": "YYYY-MM-DD",
    "created_before": "YYYY-MM-DD",
    "updated_after": "YYYY-MM-DD",
    "text_search": "string",
    "author": "string",
    "assignee": "string"
  },
  "limit": 30
}

```

## Processo 

**Passo 1: Montar a Query de Busca**

Com base nos filtros fornecidos, construir uma query no formato de busca do GitHub:

* `state:open` ou `state:closed` ou `is:open`[cite: 26]
* `label:"bug"` para cada label[cite: 26]
* `created:>=YYYY-MM-DD` e `created:<=YYYY-MM-DD` para intervalo de datas[cite: 26]
* `updated:>=YYYY-MM-DD` para atualizações[cite: 26]
* `author:username` ou `assignee:username`[cite: 26]
* O `text_search` é inserido diretamente na query[cite: 26]

Exemplo de query final:[cite: 26]

```text
repo:rezluis/todo-app is:open label:"bug" created:>=2025-01-01
```

**Passo 2: Executar a Consulta**[cite: 27]

1. Se a consulta for para um **único repositório** e filtros simples (state, labels), use a ferramenta MCP `list_issues`.[cite: 27]
2. Se a consulta for **cross-repo**, usar texto livre, ou filtros de data complexos, use `search_issues`.[cite: 27]

**Passo 3: Formatar os Resultados**[cite: 27]

Extrair e formatar os campos relevantes de cada issue:[cite: 27]

```json
{
  "total_count": 5,
  "issues": [
    {
      "number": 42,
      "title": "Erro 500 no login",
      "state": "open",
      "labels": ["bug", "triage"],
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-16T14:20:00Z",
      "author": "rezluis",
      "assignee": null,
      "body_excerpt": "Quando tento fazer login..."
    }
  ]
}

```

**Exemplo de Uso**

**Consulta: Todos os bugs abertos criados em janeiro de 2025**

```text
call skill issue-query
  owner="rezluis"
  repo="todo-app"
  filters={
    state: "open",
    labels: ["bug"],
    created_after: "2025-01-01",
    created_before: "2025-01-31"
  }

```

**Tratamento de Erros**[cite: 29]

* Se nenhuma issue for encontrada, retornar lista vazia com total_count: 0[cite: 29]
* Se o repositório não existir, retornar erro 404[cite: 29]
* Se o token não tiver permissão, retornar erro de autenticação[cite: 29]


### 2.3. Criar um Comando para Consulta (`issues.md`)

Crie um comando no seu Spec-Kit para que o usuário possa consultar issues diretamente pelo chat do OpenCode.

**Arquivo:** `commands/issues.md` (na sua extensão)

```markdown
---
description: "Lista e filtra issues do GitHub por label, data, estado e outros critérios"
---

# Comando: Consulta de Issues

Este comando permite consultar issues de um repositório GitHub com filtros personalizados.

## Entrada do Usuário
$ARGUMENTS

## Instruções para o Agente

1. **Extrair Parâmetros:** Da entrada em `$ARGUMENTS`, extraia:
   - `owner` e `repo` (do formato `owner/repo` ou da URL do repositório)
   - Filtros: `state`, `labels`, `created_after`, `created_before`, `text_search`, etc.

2. **Invocar a Skill:** Use a skill `issue-query` para executar a consulta:

call skill issue-query
owner={owner}
repo={repo}
filters={filters}


3. **Apresentar Resultados:** Formate os resultados em uma tabela legível:
| # | Título | Estado | Labels | Criado em | Autor |
|---|--------|--------|--------|-----------|-------|
| 42 | Erro 500 no login | open | bug, triage | 2025-01-15 | rezluis |

4. **Finalizar:** Informe o total de issues encontradas e pergunte se o usuário deseja ver detalhes de alguma issue específica.

## Exemplos de Uso

- `/speckit.maintenance.issues rezluis/todo-app --state open --label bug`
- `/speckit.maintenance.issues rezluis/todo-app --created-after 2025-01-01`
- `/speckit.maintenance.issues rezluis/todo-app --search "login error"`


