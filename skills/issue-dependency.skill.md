---
description: "Analisa dependências entre issues (blocked by, blocking) e constrói grafo"
mcp_servers: ["github"]
---

## Propósito
Esta skill analisa um conjunto de issues do GitHub, extrai os relacionamentos de dependência ("blocked by" e "blocking"), constrói um grafo direcionado e identifica o caminho crítico. É usada pelo agente `backlog-triage` para determinar a ordem correta de resolução.

## Entrada

```json
{
  "owner": "string",
  "repo": "string",
  "issues": [
    {
      "number": 42,
      "title": "string",
      "labels": ["string"],
      "body": "string",
      "state": "open|closed"
    }
  ],
  "include_closed": false
}

```

**Processo de Análise**[cite: 21]

**Etapa 1: Extrair Relacionamentos de Dependência**[cite: 21]

Existem duas fontes para detectar dependências entre issues. A skill deve consultar ambas.[cite: 21]

**1.1. Fonte Primária: Timeline API do GitHub**[cite: 21]

O GitHub possui um recurso nativo de dependências acessível via API. Para cada issue, consultar a timeline e procurar por eventos dos tipos:[cite: 21]

* `cross-referenced` — quando outra issue/PR referencia esta[cite: 21]
* `connected` — quando uma dependência explícita é criada[cite: 21]
* `marked_as_duplicate` — quando é marcada como duplicada[cite: 21]

**Ferramentas MCP:**[cite: 21]

* `github_get_issue_timeline` (ou `issue_read` com parâmetro de timeline) — busca os eventos da timeline da issue[cite: 21]
* Extrair de cada evento os campos `source.issue.number` e `event`[cite: 21]

**1.2. Fonte Secundária: Análise Textual**[cite: 22]

Como nem todas as dependências são registradas formalmente, analisar o texto do corpo e dos comentários em busca de padrões:[cite: 22]

| Padrão no texto | Relação detectada |
| :--- | :--- |
| `blocked by #N` | Esta issue é **bloqueada por #N** |
| `blocks #N` | Esta issue **bloqueia #N** |
| `depends on #N` | Esta issue **depende de #N** |
| `requires #N` | Esta issue **requer #N** |
| `after #N` | Esta issue vem **depois de #N** |
| `related to #N` | Relacionamento fraco (não bloqueante) |
| `duplicate of #N` | Duplicata de #N |
| `fixes #N` | Corrige #N (para PRs) |
| `closes #N` | Fecha #N |
```[cite: 22]

Regex sugerido (case-insensitive): ```text (?:blocked by|blocks|depends on|requires|after|related to|duplicate of)\s+#(\d+) ```

**1.3. Consolidação**[cite: 23]

Combinar os resultados das duas fontes em um mapa unificado. Em caso de conflito, a **timeline API tem precedência** (é mais confiável que análise textual).[cite: 23]

**Etapa 2: Construir o Grafo Direcionado**[cite: 23]

Representar as dependências como um grafo direcionado (DAG — Directed Acyclic Graph) onde:[cite: 23]

* **Nós:** Cada issue (número + metadados)[cite: 23]
* **Arestas:** Relação `blocked_by` (A é bloqueada por B $\rightarrow$ aresta B $\rightarrow$ A)[cite: 23]

**Estrutura interna do grafo:**[cite: 23]

```json
{
  "nodes": {
    "42": {"title": "...", "labels": [...], "priority_score": 0},
    "55": {"title": "...", "labels": [...], "priority_score": 0}
  },
  "edges": [
    {"from": 42, "to": 55, "type": "blocks", "source": "timeline"}
  ]
}

```

**Etapa 3: Detectar Ciclos**[cite: 24]

Ciclos em um grafo de dependências são **problemas** — significam que duas issues se bloqueiam mutuamente, o que é impossível de resolver.[cite: 24]

**Algoritmo: DFS (Depth-First Search) com coloração** (branco/cinza/preto):[cite: 24]

1. Marcar todos os nós como brancos[cite: 24]
2. Para cada nó, executar DFS:[cite: 24]
   * Marcar nó como cinza ao entrar[cite: 24]
   * Se encontrar um nó cinza, há um ciclo $\rightarrow$ reportar[cite: 24]
   * Marcar nó como preto ao sair[cite: 24]
3. Coletar todos os ciclos detectados[cite: 24]

**Saída de ciclos:**[cite: 24]

```json
"cycles": [
  {
    "issues": [42, 55, 60],
    "severity": "critical",
    "description": "Ciclo detectado: 42 -> 55 -> 60 -> 42"
  }
]

```

**Etapa 4: Calcular Métricas do Grafo**

Para cada nó, calcular:[cite: 25]

**4.1. Grau de Entrada ( `in_degree` )**[cite: 25]

Quantas issues **bloqueiam** esta issue. Quanto maior, mais dependências ela tem.[cite: 25]

**4.2. Grau de Saída ( `out_degree` )**[cite: 25]

Quantas issues **são bloqueadas** por esta. Quanto maior, mais crítica ela é (bloqueia muita coisa).[cite: 25]

**4.3. Profundidade ( `depth` )**[cite: 25]

Distância do nó até a raiz (issue sem bloqueadores). Nós com depth 0 podem começar imediatamente.[cite: 25]

**4.4. Criticidade ( `criticality` )**[cite: 25]

Fórmula sugerida:[cite: 25]

```text
criticality = out_degree * 2 + in_degree
```

Quanto maior a criticidade, mais cedo a issue deve ser resolvida.

**Etapa 5: Identificar o Caminho Crítico**

O **caminho crítico** é a sequência mais longa de dependências encadeadas, do início até o fim. Resolver issues fora desse caminho não desbloqueia o sistema.[cite: 26]

**Algoritmo: Longest Path em DAG**[cite: 26]

1. Ordenar topologicamente os nós[cite: 26]
2. Para cada nó na ordem, calcular:[cite: 26]

```text
longest_to_node[n] = max(longest_to_node[predecessor] + 1)
                     para todo predecessor de n
```
3. Rastrear o caminho de volta a partir do nó com maior valor[cite: 27]

**Saída do caminho crítico:**[cite: 27]

```json
"critical_path": {
  "issues": [42, 55, 60, 61],
  "total_length": 4,
  "reason": "Este é o caminho mais longo de dependências encadeadas"
}
```

**Etapa 6: Gerar Recomendações de Ordem**[cite: 28]

Com base no grafo, produzir uma **ordem topológica** de resolução que respeite todas as dependências. Se houver ciclos, resolvê-los primeiro.[cite: 28]

**Algoritmo de Kahn (ordenação topológica):**[cite: 28]

1. Calcular `in_degree` de cada nó[cite: 28]
2. Colocar em uma fila todos os nós com `in_degree = 0`[cite: 28]
3. Enquanto a fila não estiver vazia:[cite: 28]
   * Remover nó da fila, adicionar à ordem final[cite: 28]
   * Para cada vizinho, decrementar `in_degree`[cite: 28]
   * Se `in_degree` chegar a 0, adicionar à fila[cite: 28]
4. Se sobraram nós, há ciclo (não é possível ordenar)[cite: 28]

**Critério de desempate:** Se dois nós têm `in_degree = 0` ao mesmo tempo, priorizar o de maior `criticality`.[cite: 28]

Saida:
```json
{
  "graph": {
    "nodes": {
      "42": {
        "title": "Falha na validação de token JWT",
        "labels": ["bug", "security", "priority/P0"],
        "in_degree": 0,
        "out_degree": 1,
        "depth": 0,
        "criticality": 2
      },
      "55": {
        "title": "Erro 500 ao atualizar perfil",
        "labels": ["bug", "priority/P1"],
        "in_degree": 1,
        "out_degree": 1,
        "depth": 1,
        "criticality": 3
      }
    },
    "edges": [
      {"from": 42, "to": 55, "type": "blocks", "source": "timeline"}
    ]
  },
  "cycles": [],
  "critical_path": {
    "issues": [42, 55, 60],
    "total_length": 3,
    "reason": "Cadeia de dependências mais longa"
  },
  "topological_order": [42, 55, 60, 61, 63],
  "recommendations": [
    {
      "order": 1,
      "issue": 42,
      "reason": "Sem bloqueadores; bloqueia 1 issue de alta prioridade"
    },
    {
      "order": 2,
      "issue": 55,
      "reason": "Desbloqueada após #42; bloqueia 1 issue"
    }
  ],
  "summary": "5 issues analisadas, 4 dependências identificadas, 0 ciclos. Caminho crítico: 42 → 55 → 60."
}
```
Entrada:

```json
{
  "owner": "rezluis",
  "repo": "todo-app",
  "issues": [
    {"number": 42, "title": "Falha JWT", "labels": ["bug", "priority/P0"], "body": "..."},
    {"number": 55, "title": "Erro 500 no perfil", "labels": ["bug", "priority/P1"], "body": "blocked by #42"},
    {"number": 60, "title": "Adicionar filtro por data", "labels": ["enhancement"], "body": "depends on #55"}
  ]
}
```
Saida(resumida):

```json
{
  "critical_path": {
    "issues": [42, 55, 60],
    "total_length": 3
  },
  "topological_order": [42, 55, 60],
  "cycles": []
}
```
**Tratamento de Erros**[cite: 29]

| Erro | Ação |
| :--- | :--- |
| **Issue referenciada não existe** | Ignorar a aresta e registrar aviso |
| **Ciclo detectado** | Reportar como `severity: "critical"` e sugerir intervenção manual |
| **Timeline não acessível** | Cair para análise textual como fallback |
| **Nenhuma dependência encontrada** | Retornar grafo vazio, mas válido |
| **Lista de issues vazia** | Retornar erro de validação |

**Boas Práticas**[cite: 29]

* **Sempre validar referências:** Uma issue `#999` mencionada pode não existir[cite: 29]
* **Preservar evidências:** Toda aresta deve ter sua `source` (timeline ou texto)[cite: 29]
* **Reportar ambiguidade:** Relacionamentos "related to" são registrados mas não usados para ordenação[cite: 29]
* **Documentar ciclos:** Nunca mascarar ciclos; reportar para resolução manual[cite: 29]

