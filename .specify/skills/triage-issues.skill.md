# Triage Issues Skill

## Descrição
Skill especializada em triagem automatizada de issues de acordo com a ISO/IEC 14764:2022. Esta skill é responsável por classificar, validar e rotular issues, determinando seu tipo de manutenção e elegibilidade para processamento automático.

---

## Metadados

| Propriedade | Valor |
|:---|:---|
| **Nome** | `triage-issues` |
| **Versão** | 1.0.0 |
| **Agente Responsável** | `triage-agent` |
| **Dependências** | `iso-14764.rules.md`, `github-workflow.rules.md` |
| **Triggers** | Chamado por `process-issues.skill` |
| **Tempo Máximo de Execução** | 30 segundos |

---

## Entradas (Inputs)

### 1. Dados da Issue

| Campo | Tipo | Descrição | Exemplo |
|:---|:---|:---|:---|
| `issue_number` | integer | Número da issue no GitHub | 123 |
| `title` | string | Título da issue | "Erro ao salvar usuário com email duplicado" |
| `body` | string | Descrição completa da issue | "Ao tentar criar um usuário..." |
| `comments` | array | Lista de comentários da issue | [{"user": "joao", "body": "..."}] |
| `labels` | array | Labels atuais da issue | ["bug", "priority/high"] |
| `user` | string | Autor da issue | "joao@email.com" |
| `created_at` | datetime | Data de criação | "2025-09-02T10:00:00Z" |
| `state` | string | Estado da issue | "open" |

### 2. Configurações (via .env e rules)

```bash
# Triage Configuration
MIN_DESCRIPTION_LENGTH=20          # Tamanho mínimo da descrição
SIMILARITY_THRESHOLD=0.8           # Threshold para detectar duplicatas
MAX_ISSUES_PER_USER=5              # Limite de issues abertas por usuário

# Classification Keywords (configurável via rules)
CORRECTIVE_KEYWORDS: ["bug", "error", "crash", "fix", "exception", "fail", "broken"]
ADAPTIVE_KEYWORDS: ["update", "upgrade", "version", "dependency", "compatibility", "migration"]
PERFECTIVE_KEYWORDS: ["performance", "improve", "refactor", "optimize", "enhance", "speed"]
PREVENTIVE_KEYWORDS: ["security", "vulnerability", "patch", "risk", "audit", "compliance"]

# Priority Keywords
HIGH_PRIORITY_KEYWORDS: ["critical", "blocker", "urgent", "security", "data loss"]
