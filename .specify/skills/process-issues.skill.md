# Process Issues Skill

## Descrição
Skill orquestradora principal que gerencia todo o pipeline de manutenção de software, coordenando a execução das demais skills e agentes. Esta skill é o ponto central de controle que garante que cada issue siga o fluxo correto de triagem, análise, implementação e revisão, conforme definido pela ISO/IEC 14764:2022.

---

## Metadados

| Propriedade | Valor |
|:---|:---|
| **Nome** | `process-issues` |
| **Versão** | 1.0.0 |
| **Agente Responsável** | `gateway-agent` |
| **Dependências** | `triage-issues.skill`, `impact-analysis.skill`, `fix-issues.skill`, `babysit-prs.skill` |
| **Triggers** | Webhook, Schedule, Command |
| **Tempo Máximo de Execução** | 5 minutos (por lote) |

---

## Entradas (Inputs)

### 1. Gatilhos de Execução

| Tipo | Fonte | Exemplo |
|:---|:---|:---|
| **Webhook** | GitHub (issues.opened, issues.reopened) | Nova issue #123 aberta |
| **Schedule** | Cron job (a cada 15 minutos) | `*/15 * * * *` |
| **Command** | Comando manual no GitHub | `/process-issues` ou `/process-issue #123` |
| **Manual** | Script CLI | `./run_agent.sh process-issues` |

### 2. Configurações (via .env)

```bash
# GitHub Configuration
GITHUB_TOKEN=github_pat_xxx
REPO_OWNER=organization-name
REPO_NAME=repository-name

# Processing Configuration
PROCESS_INTERVAL=900              # 15 minutos em segundos
MAX_ISSUES_PER_BATCH=10           # Máximo de issues por execução
MAX_RETRIES=3                     # Tentativas em caso de falha
RETRY_DELAY=60                    # Segundos entre tentativas

# Auto-Fix Configuration
AUTO_FIX_ENABLED=true
MIN_TEST_COVERAGE=70              # Cobertura mínima para auto-fix
MAX_AUTO_FIX_PER_DAY=20           # Limite diário de auto-fixes

# Logging
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/process-issues.log

```

### 3. Estado Atual do Sistema

| Tipo | Fonte | Exemplo |
