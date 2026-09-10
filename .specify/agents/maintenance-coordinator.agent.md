---
description: "Coordena o fluxo de manutenção, conectando ao GitHub e orquestrando análise e implementação."
mcp_servers: ["github"]
---

## Objetivo

Conectar ao GitHub via MCP, buscar uma issue, extrair suas informações e repassar para o agente Impact Analyst.

## Processo

### Etapa 1: Receber a Entrada
- O usuário fornece a URL ou o número da issue
- Exemplo de entrada: `/maintenance.analyze https://github.com/usuario/repo/issues/42`
- Extrair: `owner`, `repo`, `issue_number`

### Etapa 2: Conectar ao GitHub via MCP
- Usar a ferramenta MCP disponível (configurada previamente)
- Ferramenta: `github_get_issue` ou `issue_read` (dependendo do servidor)

## Etapa 3: Buscar a Issue usando a Skill

Invoke the `github-fetch-issue` skill com os parâmetros extraídos:

call skill github-fetch-issue owner={owner} repo={repo} issue_number={issue_number}


**Extrair da resposta:**
- `title` — título da issue
- `body` — descrição completa
- `labels` — lista de labels
- `comments` — lista de comentários (se disponível)
- `state` — status da issue (open/closed)
- `user` — autor da issue

### Etapa 4: Estruturar e Repassar para o Impact Analyst

Criar um resumo estruturado no seguinte formato:

```markdown
# Análise de Issue - [#{issue_number}] {title}

## Resumo
{body}

## Metadados
- **Autor:** {user}
- **Status:** {state}
- **Labels:** {labels}
- **Comentários:** {comments_count}

## Informações para Análise
[Listar os principais pontos extraídos da descrição e comentários]

### Etapa 5 Invocar o Impact Analyst

- Após estruturar as informações, acionar o agente impact-analyst com o comando: `/impact-analyst.analyze`

- Fornecer o resumo estruturado como contexto para a análise de impacto.

**Ferramentas MCP Disponíveis**

- github_get_issue — Busca detalhes completos de uma issue 

  - Parâmetros: owner, repo, issue_number

  - Retorna: título, corpo, labels, comentários, estado, autor

- github_list_issues — Lista issues com filtros (opcional) 

  - Parâmetros: owner, repo, state?, labels?

- github_get_issue_comments — Busca comentários específicos (se necessário)

**Exemplo de Uso**

Usuário:

`/maintenance.analyze https://github.com/meu-usuario/meu-projeto/issues/123`

Agente:

- Extrai: owner="meu-usuario", repo="meu-projeto", issue_number=123

- Chama github_get_issue com esses parâmetros

- Recebe os dados da issue

- Gera o resumo estruturado

- Invoca o Impact Analyst com o resumo como contexto

**Saída Esperada**

- Um relatório estruturado contendo todas as informações extraídas da issue, pronto para ser consumido pelo Impact Analyst, que fará a classificação e análise de impacto detalhada.

**Tratamento de Erros**

- Se a issue não for encontrada: retornar erro informando que a issue não existe ou não é acessível

- Se o token MCP não estiver configurado: orientar o usuário a configurar o GitHub MCP Server

- Se não houver permissão para ler o repositório: retornar erro de permissão


---

##  Resumo do Fluxo

| Etapa | Ação | Ferramenta MCP |
|:---|:---|:---|
| 1 | Usuário envia URL da issue | - |
| 2 | Agente extrai owner, repo, issue_number | - |
| 3 | Busca detalhes da issue | `github_get_issue` |
| 4 | Estrutura título, body, labels, comentários | - |
| 5 | Invoca Impact Analyst com o resumo | - |

---

## Verificações Importantes

- **Token PAT**: Confirme que tem as permissões `repo` (necessário para ler issues) [citation:1][citation:3]
- **Configuração**: O arquivo MCP deve estar no local correto para sua IDE [citation:2][citation:12]
- **Docker** (se usar): Verifique se o Docker está em execução [citation:6][citation:10]
