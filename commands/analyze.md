---
description: "Analisa uma issue de manutenção no GitHub e inicia o fluxo de análise de impacto"
---

# Comando: Análise de Manutenção

Este comando inicia o fluxo de manutenção para uma issue específica do GitHub.

## Entrada do Usuário
$ARGUMENTS

## Instruções para o Agente

Você deve executar o seguinte fluxo de trabalho:

1.  **Extrair a URL da Issue:** Da entrada fornecida em `$ARGUMENTS`, extraia o `owner`, o `repo` e o `issue_number`.
2.  **Buscar a Issue:** Use a skill `github-fetch-issue` para buscar os dados da issue no GitHub via MCP.
3.  **Classificar a Manutenção:** Com os dados da issue, use a skill `classify-maintenance`.
4.  **Avaliar o Impacto:** Com a classificação, use a skill `impact-assessment`.
5.  **Gerar Relatório:** Combine os resultados e salve em `.specify/maintenance/analysis/`.
6.  **Finalizar:** Informe ao usuário que a análise foi concluída.
