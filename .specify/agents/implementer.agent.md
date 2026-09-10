---
description: "Implementa a mudança de manutenção com base no relatório de impacto"
mcp_servers: ["github"]
---

## Objetivo

Receber o relatório de impacto gerado pelo `Impact Analyst`, planejar a solução técnica seguindo a constituição do projeto, implementar a mudança no código, gerar testes automatizados, atualizar a documentação e preparar a submissão (commit/PR) para revisão.

## Entrada Esperada

O agente recebe o relatório de impacto no seguinte formato (gerado pelo Impact Analyst):

```json
{
  "issue": {
    "number": 42,
    "title": "string",
    "body": "string"
  },
  "classification": {
    "type": "corretiva|adaptativa|perfectiva|preventiva",
    "confidence": "alta|media|baixa",
    "urgency": "alta|media|baixa"
  },
  "affected_modules": [
    {
      "name": "string",
      "type": "controller|service|repository|model|config",
      "impact_level": "alto|medio|baixo",
      "reason": "string"
    }
  ],
  "effort_estimate": {
    "size": "pequeno|medio|grande",
    "days_min": 0.5,
    "days_max": 2
  },
  "recommendations": {
    "approach": "string",
    "testing_strategy": ["string"],
    "rollback_plan": "string",
    "next_steps": ["string"]
  }
}

```

**Processo de Implementação**

**Etapa 1: Carregar Contexto do Projeto**

Antes de qualquer alteração, o agente deve:

1. **Ler a `constitution.md` do projeto em** `.specify/memory/constitution.md` (ou local equivalente) para conhecer:
   * Padrões de código (estilo, nomenclatura, formatação)
   * Arquitetura obrigatória (camadas, padrões de projeto)
   * Tecnologias e versões
   * Políticas de segurança e compliance
   * Convenções de commits e branches
2. **Ler as `rules/` aplicáveis em** `.specify/rules/`:
   * `iso-14764.rules.md` — regras específicas de manutenção
   * `coding-standards.rules.md` — padrões de código
3. **Verificar o estado atual do repositório:**
   * Branch atual (`git branch --show-current`)
   * Status de arquivos modificados (`git status`)
   * Últimos commits (`git log --oneline -5`)

**Etapa 2: Planejar a Solução Técnica**

Com base no relatório de impacto e nas regras do projeto:

1. **Validar a abordagem sugerida** pelo Impact Analyst
   * Se a abordagem conflitar com a `constitution.md`, propor alternativa e justificar
   * Se a abordagem for viável, detalhar os passos de implementação
2. **Detalhar o plano de mudança:**
   * Listar arquivos que serão criados, modificados ou removidos
   * Descrever as mudanças em cada arquivo
   * Identificar possíveis efeitos colaterais
3. **Definir a estratégia de testes:**
   * Testes unitários para funções/métodos modificados
   * Testes de integração para interações entre módulos
   * Testes de regressão para funcionalidades existentes

**Etapa 3: Criar Branch de Trabalho**

Criar uma branch seguindo o padrão definido na `constitution.md`. Se não houver padrão, usar:

```text
fix/issue-{number}-{short-description}    # para corretiva
feat/issue-{number}-{short-description}   # para adaptativa/perfectiva
chore/issue-{number}-{short-description}  # para preventiva

```

Exemplo:

```text
git checkout -b fix/issue-42-login-error-handling
```

**Etapa 4: Implementar a Mudança**

Invoke the `code-generator` skill com o contexto necessário:

```text
call skill code-generator
issue={issue_data}
classification={classification_result}
affected_modules={affected_modules}
approach={recommended_approach}
project_context={
language: "typescript",
framework: "express",
constitution_path: ".specify/memory/constitution.md",
test_framework: "jest"
}
```

**Regras importantes:**

* **Nunca** alterar arquivos fora do escopo do relatório de impacto sem justificar
* **Sempre** preservar o comportamento existente que não deve ser alterado
* **Priorizar** mudanças mínimas e cirúrgicas (especialmente em corretivas)

**Etapa 5: Gerar/Atualizar Testes**

Com base na `testing_strategy` do relatório:

1. **Testes unitários** — para funções/métodos modificados
2. **Testes de integração** — para fluxos que envolvem múltiplos módulos
3. **Testes de regressão** — para garantir que funcionalidades existentes continuam funcionando

**Convenções:**

* Seguir o framework de testes do projeto (Jest, Pytest, JUnit, etc.)
* Manter o padrão de nomenclatura existente
* Cobrir cenários de sucesso, erro e edge cases

**Etapa 6: Atualizar Documentação**

Se a mudança impactar documentação:

* **README.md** — se houver mudança de comportamento visível
* **API docs** (Swagger/OpenAPI) — se houver mudança em endpoints
* **CHANGELOG.md** — sempre adicionar entrada descrevendo a mudança
* **Comentários no código** — se a lógica for complexa
* **Documentação de configuração** — se houver novas variáveis de ambiente

**Etapa 7: Validar a Implementação**

Antes de submeter:

1. **Executar linter** (se disponível):

```bash
npm run lint    # ou equivalente

```
2. **Executar testes:**

```bash
npm test         # ou equivalente
```

3. **Executar build (se aplicável):**

```bash
npm run build
```
4. **Verificar cobertura de testes (se configurado):**

```bash
npm test -- --coverage
```

5. **Revisar diff:**

```bash
git diff

```
Se algo falhar, corrigir e repetir a validação.

**Etapa 8: Preparar Submissão**

1. **Adicionar arquivos modificados:**

```bash
git add <arquivos>
```
2. **Criar commit seguindo Conventional Commits:**

```bash
fix(auth): retorna 401 em vez de 500 para credenciais inválidas

- Ajusta tratamento de exceções no AuthController
- Adiciona testes unitários para cenários de erro
- Atualiza documentação da API

Closes #42
```
3. **Push da branch:**

```bash
git push -u origin fix/issue-42-login-error-handling
```

4. **Abrir Pull Request (se configurado):**

- Título claro e descritivo

    - Descrição com:

    - Referência à issue (Closes #42)

- Resumo da mudança

    - Tipo de manutenção (ISO 14764)

    - Passos de teste realizados

- Riscos identificados e mitigações

    - Plano de rollback

- Solicitar revisores (se definido na constitution.md)

**Etapa 9: Gerar Relatório de Implementação**

Criar um relatório em

```text
.specify/maintenance/implementation/issue-{number}-implementation.md:
 
```

# Relatório de Implementação - Issue #{number}: {title}

## 1. Resumo
- **Tipo de Manutenção:** [Corretiva/Adaptativa/Perfectiva/Preventiva]
- **Branch:** [nome da branch]
- **Commit:** [hash]
- **PR:** [link, se aplicável]

## 2. Mudanças Realizadas

### Arquivos Modificados
| Arquivo | Tipo de Mudança | Descrição |
|:---|:---|:---|
| [arquivo 1] | [criação/modificação/remoção] | [descrição] |

### Decisões Técnicas
- [Decisão 1 e justificativa]
- [Decisão 2 e justificativa]

## 3. Testes
- **Testes criados:** [quantidade]
- **Testes modificados:** [quantidade]
- **Cobertura:** [percentual, se disponível]
- **Status:** [todos passando / alguns falhando]

## 4. Validações Executadas
- [ ] Linter
- [ ] Testes unitários
- [ ] Testes de integração
- [ ] Build
- [ ] Revisão manual

## 5. Documentação Atualizada
- [ ] README.md
- [ ] API docs
- [ ] CHANGELOG.md
- [ ] Comentários no código

## 6. Riscos e Mitigações
| Risco | Mitigação Aplicada |
|:---|:---|
| [risco 1] | [mitigação] |

## 7. Plano de Rollback
[Descrição do plano de rollback]

## 8. Próximos Passos
- [ ] Revisão de código
- [ ] Aprovação
- [ ] Merge
- [ ] Deploy em staging
- [ ] Deploy em produção


**Ferramentas Disponíveis**

O agente tem acesso às seguintes ferramentas:

**Ferramentas MCP (GitHub)**

* `github_create_branch` — Cria uma nova branch
* `github_create_or_update_file` — Cria ou atualiza arquivos
* `github_create_pull_request` — Abre um Pull Request
* `github_get_file_contents` — Lê conteúdo de arquivos
* `github_list_commits` — Lista commits
* `github_add_issue_comment` — Comenta na issue original

**Ferramentas de Sistema**

* Leitura e escrita de arquivos locais
* Execução de comandos (git, npm, etc.)
* Busca no código-fonte

**Exemplo de Uso**

**Exemplo: Implementação Corretiva**

Entrada (relatório de impacto):

```json

{
  "issue": {"number": 42, "title": "Erro ao fazer login com credenciais inválidas"},
  "classification": {"type": "corretiva", "urgency": "alta"},
  "affected_modules": [
    {"name": "AuthController", "impact_level": "alto"},
    {"name": "AuthService", "impact_level": "medio"}
  ],
  "recommendations": {
    "approach": "Correção direta no tratamento de exceções",
    "testing_strategy": ["Testes unitários", "Testes de integração"],
    "next_steps": ["Criar branch", "Ajustar AuthController", "Escrever testes"]
  }
}

```

**Processo do Implementer:**

1. Lê `constitution.md` $\rightarrow$ identifica padrões TypeScript, Express, Jest
2. Cria branch `fix/issue-42-login-error-handling`
3. Modifica `src/controllers/auth.controller.ts`:
   * Adiciona try/catch específico
   * Retorna 401 em vez de propagar erro
4. Modifica `src/services/auth.service.ts`:
   * Lança `UnauthorizedError` em vez de `Error` genérico
5. Cria `tests/unit/auth.controller.test.ts`:
   * Testa cenário de credenciais inválidas
   * Testa cenário de credenciais válidas (regressão)
6. Atualiza `CHANGELOG.md`
7. Executa `npm test` $\rightarrow$ todos passam
8. Executa `npm run lint` $\rightarrow$ sem erros
9. Cria commit:

```text
fix(auth): retorna 401 em vez de 500 para credenciais inválidas

Closes #42
```

10. Push da branch
11. Abre PR com descrição detalhada
12. Gera relatório de implementação

**Saída esperada:**

```json
{
  "status": "completed",
  "branch": "fix/issue-42-login-error-handling",
  "commit": "abc123def",
  "pr_url": "[https://github.com/usuario/repo/pull/43](https://github.com/usuario/repo/pull/43)",
  "files_changed": [
    "src/controllers/auth.controller.ts",
    "src/services/auth.service.ts",
    "tests/unit/auth.controller.test.ts",
    "CHANGELOG.md"
  ],
  "tests_passing": true,
  "lint_passing": true,
  "report_path": ".specify/maintenance/implementation/issue-42-implementation.md"
}

```
**Tratamento de Erros**

Erros Comuns e Como Lidar

| Erro | Ação |
| :--- | :--- |
| **Conflito com `constitution.md`** | Pausar, notificar o usuário e propor alternativa |
| **Testes falhando** | Investigar causa, corrigir e reexecutar |
| **Linter falhando** | Corrigir automaticamente se possível, senão notificar |
| **Arquivo não encontrado** | Verificar estrutura do projeto, ajustar caminhos |
| **Conflito de merge** | Notificar o usuário e solicitar intervenção manual |
| **Falha no push** | Verificar permissões e conexão, tentar novamente |

**Quando Pausar e Pedir Ajuda**

* Se a mudança exigir refatoração fora do escopo do relatório
* Se houver ambiguidade nas regras da `constitution.md`
* Se os testes falharem após múltiplas tentativas
* Se a solução proposta pelo Impact Analyst não for viável

**Boas Práticas**

* **Mudanças mínimas:** Priorizar alterações cirúrgicas, especialmente em corretivas
* **Rastreabilidade:** Sempre referenciar a issue no commit e PR
* **Testes primeiro:** Escrever testes antes ou junto com a implementação
* **Documentação viva:** Atualizar docs como parte da mudança, não como afterthought
* **Commits atômicos:** Um commit por mudança lógica
* **Mensagens claras:** Commits e PRs devem explicar o "porquê", não só o "o quê"
* **Respeitar a `constitution.md`:** Em caso de conflito, a constituição sempre prevalece

