---
description: "Busca uma issue do GitHub usando MCP"
mcp_servers: ["github"]
---

## Propósito
Esta skill encapsula a lógica de buscar uma issue específica do GitHub via MCP e retornar seus dados estruturados.

## Entrada
- `owner` (string): Dono do repositório
- `repo` (string): Nome do repositório
- `issue_number` (number): Número da issue

## Processo

### Passo 1: Chamar a Ferramenta MCP
Utilize a ferramenta `github_get_issue` (ou `get_issue` dependendo do servidor) com os seguintes parâmetros:

Ferramenta: `github_get_issue`
Parâmetros: owner: `owner` , `repo: {repo}`, `issue_number: {issue_number}`.


### Passo 2: Extrair os Dados da Resposta
Da resposta da ferramenta, extraia os seguintes campos:
- `title` — título da issue
- `body` — descrição completa
- `labels` — array de labels (cada label tem um `name`)
- `comments` — array de comentários (cada comentário tem `user.login` e `body`)
- `state` — status da issue (`"open"` ou `"closed"`)
- `user` — autor da issue (`user.login`)

### Passo 3: Estruturar a Saída
Retorne um objeto JSON com a seguinte estrutura:

```json
{
  "title": "string",
  "body": "string",
  "labels": ["string"],
  "comments": [
    {
      "user": "string",
      "body": "string"
    }
  ],
  "state": "string",
  "user": "string"
}

```

**Exemplo de Uso**

Chamada da skill: ` call skill github-fetch-issue owner="meu-usuario" repo="meu-projeto" issue_number=42 `

**Resposta esperada:**

```json
{
  "title": "Bug no login",
  "body": "Usuários não conseguem fazer login quando...",
  "labels": ["bug", "high-priority"],
  "comments": [
    {"user": "joao", "body": "Também estou vendo isso..."},
    {"user": "maria", "body": "Já corrigi em outro PR..."}
  ],
  "state": "open",
  "user": "ana"
}

```
**Tratamento de Erros**

- Se a issue não for encontrada (status 404): retornar erro informando que a issue não existe

- Se o token MCP não tiver permissão: retornar erro de autenticação

- Se os parâmetros estiverem incompletos: retornar erro de validação

**Dicas para o Agente**

- Certifique-se de usar o nome correto da ferramenta MCP. Teste com list_tools primeiro para ver os nomes disponíveis.

- Se a ferramenta retornar um objeto aninhado (ex: data.issue), acesse a propriedade correta.

- Os comentários podem vir em uma chamada separada (github_get_issue_comments). Verifique se a resposta já inclui os comentários ou se precisa de uma segunda chamada.
