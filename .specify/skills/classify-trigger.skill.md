# classify-trigger.skill

## Descrição Geral

A skill `classify-trigger` é responsável por receber gatilhos brutos de diversas fontes (logs de erro, issues, emails, solicitações de mudança, etc.), interpretá-los, classificar o tipo de manutenção e estruturar os dados em um formato padronizado para os demais agentes.

Esta é a primeira etapa do fluxo de manutenção e define a qualidade de toda a cadeia subsequente.

---

## Entradas

### `trigger_raw` (Obrigatório)
**Descrição:** O gatilho bruto recebido da fonte original.

| Tipo | Formato Esperado | Exemplo |
|:---|:---|:---|
| **Log de erro** | String contendo stack trace | `"java.lang.NullPointerException: Cannot invoke ..."` |
| **Issue** | Objeto JSON da API GitHub/GitLab | `{"title": "Bug no cadastro", "body": "..."}` |
| **Email** | String com conteúdo do email | `"Prezados, o sistema está permitindo datas futuras..."` |
| **Bugzilla** | String com descrição do bug | `"BUG-123: Ao criar tarefa com data futura..."` |
| **Solicitação textual** | Descrição livre | `"Precisamos implementar exportação de PDF"` |
| **Alerta de segurança** | Relatório de ferramenta | `"CVE-2021-44228 detected in log4j"` |

### `source_type` (Opcional)
**Descrição:** Tipo da fonte do gatilho (usado para otimizar o parsing). Se não fornecido, a skill tenta detectar automaticamente.

**Valores possíveis:** `log`, `issue`, `email`, `bugzilla`, `text`, `security_alert`

**Padrão:** `null` (detecção automática)

---

## Saídas

### `classification_result` (JSON)
**Descrição:** Resultado estruturado da classificação, pronto para ser consumido pelo Gateway Agent e subsequentemente pelo Impact Analysis Agent.

```
{
  "tipo_manutencao": "corretiva | adaptativa | perfectiva | preventiva",
  "prioridade": "alta | media | baixa",
  "descricao": "string",
  "contexto_adicional": "string | null",
  "arquivos_afetados": ["path/to/file.java"],
  "referencias": ["#issue-123", "log-abc"],
  "evidencias": ["https://github.com/org/repo/issues/123"],
  "palavras_chave": ["NullPointerException", "TaskService"],
  "sugestao_causa": "string | null",
  "dificuldade_estimada": "baixa | media | alta",
  "classificacao_secundaria": {
    "impacto": "baixo | medio | alto",
    "urgencia": "baixa | media | alta"
  },
  "metadata": {
    "fonte": "log | issue | email | bugzilla | text | security_alert",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

```
