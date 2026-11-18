---
description: "Analisa o backlog de issues e gera relatório de triagem priorizado"
---

# Comando: Triagem de Backlog

Analisa um conjunto de issues abertas, prioriza por impacto/urgência, detecta dependências e gera um plano de ação.

## Entrada do Usuário
$ARGUMENTS

## Instruções para o Agente

1. **Extrair Parâmetros:** De `$ARGUMENTS`, extraia `owner`, `repo` e filtros opcionais (labels, limit, state).

2. **Invocar o Agente:** Acione o agente `backlog-triage` com os parâmetros:

```text

owner={owner}
repo={repo}
filters={filters}
options={include_impact_assessment: true, max_issues_to_analyze: 50}

```

3. **Aguardar Conclusão:** O agente executará as 8 etapas do processo de triagem.

4. **Apresentar Resumo:** Ao final, exiba:
- Caminho do relatório gerado
- Top 3 prioridades com justificativa
- Alertas (ciclos, conflitos)
- Próximos passos sugeridos

## Exemplos de Uso

- `/speckit.maintenance.triage rezluis/todo-app`
- `/speckit.maintenance.triage rezluis/todo-app --labels bug,security`
- `/speckit.maintenance.triage rezluis/todo-app --limit 30`


