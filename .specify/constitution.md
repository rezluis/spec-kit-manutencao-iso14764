# Constituição do Spec-Kit de Manutenção ISO/IEC 14764

## Princípios Fundamentais

1. **Conformidade com a ISO/IEC 14764:2022**
   - Todas as atividades de manutenção devem seguir as categorias: Corretiva, Adaptativa, Perfectiva, Preventiva.
   - As atividades obrigatórias são: Análise de Problemas, Implementação de Modificações, Revisão/Aceitação.

2. **Human-in-the-Loop Obrigatório**
   - Todo plano de mudança deve ser aprovado por um humano antes da implementação.
   - O agente não pode fazer deploy em produção sem revisão humana.

3. **Preservação da Arquitetura**
   - Agentes não podem reestruturar camadas (Controller, Service, Repository) sem autorização explícita.
   - Mudanças devem respeitar os padrões de projeto existentes (ex: injeção de dependências, DTOs).

4. **Rastreabilidade**
   - Cada mudança deve ser vinculada a um gatilho (issue, log, solicitação).
   - O histórico de decisões (análise de impacto, plano, revisão) deve ser documentado.

5. **Qualidade e Testes**
   - Cobertura de testes não pode diminuir após a manutenção.
   - Todos os testes existentes devem passar antes da abertura do PR.

6. **Tecnologias Suportadas (Piloto)**
   - Backend: Java 17+, Spring Boot 3.x, Maven/Gradle.
   - Testes: JUnit 5, Mockito, Spring Boot Test.
   - Repositório: Git (GitHub/GitLab).

## Restrições Operacionais

- Os agentes devem usar exclusivamente modelos de IA gratuitos ou de baixo custo (ex: versões small de LLMs).
- As operações de clone, commit e push devem ser feitas via Git CLI ou API.
- Logs de execução devem ser armazenados para auditoria.

## Fluxo de Trabalho Obrigatório

1. Gatilho → Classificação (Gateway Agent)
2. Entendimento da Arquitetura (Architecture Agent) → `architecture-spec.md`
3. Análise de Impacto (Impact Agent) → `impact-report.md` + `change-plan.md`
4. **Aprovação Humana** (ponto de checagem)
5. Implementação (Implementation Agent) → código + testes
6. Validação (Validation Agent) → relatório de testes + cobertura
7. Criação de PR (PR Agent) → Pull Request
