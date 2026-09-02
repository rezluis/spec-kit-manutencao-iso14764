# Babysit PRs Skill

## Descrição
Skill especializada em monitorar, gerenciar e cuidar de Pull Requests abertos. Esta skill atua como uma "babá" de PRs, garantindo que eles sejam revisados, testados e gerenciados adequadamente durante todo o ciclo de vida, desde a abertura até o merge ou fechamento.

---

## Metadados

| Propriedade | Valor |
|:---|:---|
| **Nome** | `babysit-prs` |
| **Versão** | 1.0.0 |
| **Agente Responsável** | `reviewer` |
| **Dependências** | `reviewer.agent.md`, `iso-14764.rules.md` |
| **Triggers** | Agendamento (a cada 5 minutos), Webhook de PR, Comando manual |
| **Tempo Máximo de Execução** | 2 minutos |

---

## Entradas (Inputs)

### 1. Dados do PR

| Campo | Tipo | Descrição | Exemplo |
|:---|:---|:---|:---|
| `pr_number` | integer | Número do PR no GitHub | 456 |
| `title` | string | Título do PR | "[FIX] Issue #123 - Erro ao salvar usuário" |
| `body` | string | Descrição do PR | "## 🔧 Fix Issue #123..." |
| `state` | string | Estado do PR | "open" |
| `head_branch` | string | Branch de origem | "fix/issue-123" |
| `base_branch` | string | Branch de destino | "main" |
| `created_at` | datetime | Data de criação | "2025-09-02T14:35:00Z" |
| `updated_at` | datetime | Última atualização | "2025-09-02T15:00:00Z" |
| `user` | string | Autor do PR | "implementer[bot]" |
| `labels` | array | Labels do PR | ["agent/fix-pending"] |

### 2. Dados da Issue Vinculada

| Campo | Tipo | Descrição | Exemplo |
|:---|:---|:---|:---|
| `issue_number` | integer | Número da issue | 123 |
| `maintenance_type` | string | Tipo de manutenção | "corrective" |
| `priority` | string | Prioridade | "high" |

### 3. Configurações (via .env)

```bash
# Babysit Configuration
BABYSIT_INTERVAL=300                # Intervalo em segundos (5 minutos)
PR_STALE_DAYS=7                     # Dias para considerar PR stale
PR_ABANDONED_DAYS=14                # Dias para considerar PR abandonado
AUTO_MERGE_ENABLED=false            # Habilitar merge automático
MERGE_STRATEGY="squash"             # Estratégia de merge
MIN_APPROVALS=1                     # Número mínimo de aprovações
MAX_REVIEW_COMMENTS=10              # Máximo de comentários por revisão
AUTO_CLOSE_ABANDONED=false          # Fechar PRs abandonados automaticamente

# Review Configuration
REVIEW_MODEL="claude-3-sonnet"      # Modelo para revisão de código
REVIEW_TIMEOUT=60                   # Timeout em segundos para revisão
REVIEW_FOCUS_AREAS=["security", "performance", "style", "tests"]
