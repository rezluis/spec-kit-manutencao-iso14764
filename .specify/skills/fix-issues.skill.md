# Fix Issues Skill

## Descrição
Skill especializada em implementar correções automatizadas para issues validadas e analisadas. Esta skill é responsável por gerar código, criar branches, executar testes, abrir Pull Requests e gerenciar todo o fluxo de implementação de correções.

---

## Metadados

| Propriedade | Valor |
|:---|:---|
| **Nome** | `fix-issues` |
| **Versão** | 1.0.0 |
| **Agente Responsável** | `implementer` |
| **Dependências** | `impact-analysis.skill`, `iso-14764.rules.md` |
| **Triggers** | Chamado por `process-issues.skill` após análise positiva |
| **Tempo Máximo de Execução** | 5 minutos |

---

## Entradas (Inputs)

### 1. Dados da Issue

| Campo | Tipo | Descrição | Exemplo |
|:---|:---|:---|:---|
| `issue_number` | integer | Número da issue no GitHub | 123 |
| `title` | string | Título da issue | "Erro ao salvar usuário com email duplicado" |
| `body` | string | Descrição completa | "Ao tentar criar um usuário..." |
| `maintenance_type` | string | Tipo de manutenção | "corrective" |

### 2. Dados da Análise de Impacto

| Campo | Tipo | Descrição | Exemplo |
|:---|:---|:---|:---|
| `affected_files` | array | Arquivos a modificar | ["src/models/user.py"] |
| `affected_functions` | array | Funções a modificar | ["create_user", "validate_email"] |
| `action_plan` | object | Plano de ação detalhado | { "steps": [...] } |
| `risk_level` | string | Nível de risco | "low" |

### 3. Configurações (via .env)

```bash
# Fix Implementation Configuration
FIX_BRANCH_PREFIX="fix/issue-"        # Prefixo para branches de correção
PR_TITLE_PREFIX="[FIX]"               # Prefixo para títulos de PR
COMMIT_MESSAGE_PREFIX="fix:"          # Prefixo para mensagens de commit
MAX_FILES_PER_PR=10                   # Máximo de arquivos por PR
AUTO_MERGE_ENABLED=false              # Habilitar merge automático
MERGE_STRATEGY="squash"               # Estratégia de merge: squash, rebase, merge
REQUIRE_APPROVALS=1                   # Número mínimo de aprovações

# Code Generation
CODE_GENERATION_MODEL="claude-3-opus" # Modelo para geração de código
MAX_CODE_LINES=500                    # Máximo de linhas por arquivo gerado
TEST_GENERATION_ENABLED=true          # Gerar testes automaticamente
DOCUMENTATION_UPDATE_ENABLED=true     # Atualizar documentação
