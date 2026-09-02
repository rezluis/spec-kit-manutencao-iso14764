**Spec Kit de Manutenção de Software (ISO/IEC 14764)**

Kit de agentes inteligentes para automação do processo de manutenção de software, alinhado à norma **ISO/IEC/IEEE 14764:2022**, integrado com GitHub Issues e construído sobre o GitHub Spec Kit.

📂 Estrutura de Diretórios

```
spec-kit-manutencao/
├── .specify/                          # Configuração do Spec Kit e agentes
│   ├── constitution.md                # Princípios e guardrails do projeto
│   ├── agents/                        # Agentes de IA (instruções em Markdown)
│   │   ├── gateway-agent.agent.md      # Classifica a issue e inicia o fluxo
│   │   ├── impact-analyst.agent.md    # Analisa impacto da mudança
│   │   └── implementer.agent.md       # Gera a correção (rascunho do PR)
│   ├── skills/                        # Skills (procedimentos reutilizáveis)
│   │   └── github-fetcher.skill.md    # Instrução para usar o script de integração
│   └── rules/                         # Regras automáticas (carregadas por todos os agentes)
│       └── iso-14764.rules.md         # Etapas obrigatórias segundo a norma
├── src/
│   └── integrations/
│       └── github_client.py           # Código Python para buscar issues via API
├── docs/
│   ├── process-model.md               # Descrição detalhada do fluxo de manutenção
│   └── templates/
│       └── impact-report.template.md  # Template para o relatório de impacto
├── specs/                             # Artefatos gerados (especificações)
│   └── changes/                       # Cada manutenção vira uma subpasta
│       └── ISSUE-{numero}/
│           ├── spec.md                # Especificação da correção
│           └── impact-analysis.md     # Relatório de impacto gerado
├── .env.example                       # Exemplo de variáveis de ambiente
└── README.md

```
**Fluxo Principal**

```mermaid
    A[Início: Issue aberta no GitHub] --> B[Dev invoca /maintenance.triage ISSUE-123]
    
    B --> C{Agente: triage-agent<br/>Carrega regras da ISO}
    
    C --> D[Executa skill github-fetcher]
    D --> E[Chama script Python<br/>src/integrations/github_client.py]
    E --> F[Script retorna dados da Issue<br/>via API REST do GitHub]
    
    F --> G[Agente classifica a Issue<br/>Corretiva / Adaptativa / Perfectiva / Preventiva]
    G --> H[Gera artefato inicial<br/>specs/changes/ISSUE-123/impact-analysis.md]
    
    H --> I{Dev revisa classificação}
    I -->|Aprova| J[Invoca /maintenance.analyze ISSUE-123]
    I -->|Rejeita| K[Dev ajusta manualmente o relatório]
    K --> J
    
    J --> L{Agente: impact-analyst}
    L --> M[Analisa módulos afetados<br/>com base na issue e no código fonte local]
    M --> N[Atualiza o relatório de impacto<br/>com estimativa de esforço e dependências]
    
    N --> O{Dev aprova a análise?}
    O -->|Não| P[Dev solicita ajustes à IA]
    P --> L
    O -->|Sim| Q[Invoca /maintenance.implement ISSUE-123]
    
    Q --> R{Agente: implementer}
    R --> S[Lê a especificação em spec.md]
    S --> T[Gera código de correção<br/>respeitando regras de codificação]
    T --> U[Cria testes unitários para validar a correção]
    U --> V[Gera pull request no GitHub<br/>com referência à issue]
    
    V --> W[Dev revisa PR]
    W --> X{Fim}
    
```

