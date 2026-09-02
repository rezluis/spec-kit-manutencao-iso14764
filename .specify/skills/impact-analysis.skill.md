# Impact Analysis Skill

## Descrição
Skill especializada em analisar o impacto de mudanças solicitadas em issues, examinando o código-fonte, identificando dependências, avaliando riscos e gerando relatórios detalhados para orientar a implementação. Esta skill é fundamental para decisões de auto-fix e planejamento de correções.

---

## Metadados

| Propriedade | Valor |
|:---|:---|
| **Nome** | `impact-analysis` |
| **Versão** | 1.0.0 |
| **Agente Responsável** | `impact-analyst` |
| **Dependências** | `iso-14764.rules.md`, `github-workflow.rules.md` |
| **Triggers** | Chamado por `process-issues.skill` após triagem válida |
| **Tempo Máximo de Execução** | 60 segundos |

---

## Entradas (Inputs)

### 1. Dados da Issue (Triada)

| Campo | Tipo | Descrição | Exemplo |
|:---|:---|:---|:---|
| `issue_number` | integer | Número da issue no GitHub | 123 |
| `title` | string | Título da issue | "Erro ao salvar usuário com email duplicado" |
| `body` | string | Descrição completa da issue | "Ao tentar criar um usuário..." |
| `maintenance_type` | string | Tipo de manutenção (ISO 14764) | "corrective" |
| `triage_labels` | array | Labels da triagem | ["type/bug", "priority/medium"] |

### 2. Dados do Repositório

| Dado | Origem | Descrição |
|:---|:---|:---|
| **Código-fonte** | Repositório GitHub | Arquivos do projeto |
| **Estrutura de arquivos** | Repositório GitHub | Árvore de diretórios |
| **Dependências** | Arquivos de configuração | package.json, requirements.txt, etc. |
| **Testes existentes** | Diretório tests/ | Testes unitários e de integração |

### 3. Configurações (via .env e rules)

```bash
# Impact Analysis Configuration
MAX_FILES_TO_ANALYZE=20           # Máximo de arquivos a analisar
MAX_CODE_LENGTH_PER_FILE=1000     # Máximo de linhas por arquivo
MIN_TEST_COVERAGE_THRESHOLD=70    # Cobertura mínima para auto-fix
RISK_SCORE_THRESHOLD=5            # Limite de risco para auto-fix

# Complexity Weights
FILE_CHANGE_WEIGHT=1.5            # Peso por arquivo alterado
FUNCTION_CHANGE_WEIGHT=2.0        # Peso por função alterada
DEPENDENCY_WEIGHT=3.0             # Peso por dependência afetada
TEST_COVERAGE_WEIGHT=2.5          # Peso da cobertura de testes
HISTORICAL_BUGS_WEIGHT=2.0        # Peso de bugs históricos
