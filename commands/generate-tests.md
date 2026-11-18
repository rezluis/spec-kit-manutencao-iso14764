---
description: "Gera testes automatizados para uma issue, arquivo ou funcionalidade específica"
---

# Comando: Gerar Testes

Gera testes automatizados a partir de uma issue, um arquivo de código ou uma funcionalidade específica, seguindo o princípio de geração independente (os testes são derivados da especificação, não do código).

## Entrada do Usuário
$ARGUMENTS

## Modos de Uso

Este comando suporta três modos de operação:

### Modo 1: A partir de uma Issue
Gera testes com base nos critérios de aceitação descritos na issue.
/speckit.maintenance.generate-tests issue https://github.com/owner/repo/issues/42


### Modo 2: A partir de um Arquivo
Gera testes para um arquivo de código específico.
/speckit.maintenance.generate-tests file src/controllers/auth.controller.ts


### Modo 3: A partir de uma Funcionalidade
Gera testes para uma funcionalidade descrita textualmente.
/speckit.maintenance.generate-tests feature "validação de email no cadastro de usuário"


## Processo de Execução

### Etapa 1: Identificar o Modo e Coletar Contexto

Com base em `$ARGUMENTS`, determine o modo:

- **Issue:** Extrair `owner`, `repo`, `issue_number` da URL e usar a skill `github-fetch-issue` para buscar os dados.
- **File:** Ler o arquivo diretamente do repositório local.
- **Feature:** Usar a descrição textual como especificação.

### Etapa 2: Ler a Constituição e Padrões do Projeto

Antes de gerar qualquer teste, ler obrigatoriamente:

1. `.specify/memory/constitution.md` — regras do projeto (linguagem, framework, cobertura mínima)
2. `rules/coding-standards.rules.md` — convenções de código
3. Arquivos de teste existentes em `tests/` — para seguir o padrão (framework, estrutura, mocks)

### Etapa 3: Invocar a Skill `test-generator`

Passar o contexto coletado para a skill:

```text
call skill test-generator
issue={issue_data ou null}
feature_description={descrição ou null}
source_file={caminho ou null}
changes_made={null} # não há mudanças, apenas geração
review_report={null} # não há revisão prévia
project_context={
language: "...",
framework: "...",
test_framework: "...",
existing_tests_path: "tests/",
coverage_requirement: 80
}
```


**Instrução crítica para a skill:**
> Gere os testes a partir da **especificação** (issue, feature ou interface pública do arquivo), NÃO a partir da implementação. Se o arquivo de origem contém a lógica, use apenas sua **assinatura pública** e o **comportamento esperado**, não o corpo da função.

### Etapa 4: Salvar os Testes

Os testes devem ser salvos seguindo o padrão do projeto:

- **Testes unitários:** `tests/unit/{nome-do-arquivo}.test.{ext}`
- **Testes de integração:** `tests/integration/{nome-da-feature}.test.{ext}`
- **Testes de contrato:** `tests/contract/{nome-do-endpoint}.test.{ext}`

Se os arquivos já existirem, **perguntar ao usuário** antes de sobrescrever:
- Opção 1: Sobrescrever
- Opção 2: Criar arquivo com sufixo `.new`
- Opção 3: Fazer merge dos testes

### Etapa 5: Validar Sintaxe

Verificar que os testes:
- Compilam (para linguagens tipadas)
- Têm imports corretos
- Referenciam símbolos existentes
- Não contêm erros de sintaxe óbvios

### Etapa 6: Apresentar Resumo

Exibir ao usuário:

## Testes Gerados

### Arquivos Criados
- `tests/unit/auth.controller.test.ts` — 5 casos de teste

### Cenários Cobertos
- ✅ Happy path: login com credenciais válidas
- ✅ Erro: credenciais inválidas retornam 401
- ✅ Erro: campos ausentes retornam 400
- ✅ Borda: senha vazia
- ✅ Regressão: outros endpoints não afetados

### Cobertura Estimada
- Estimativa: +3.5% de cobertura
- Total projetado: 81%

### Próximos Passos
1. Revisar os testes gerados
2. Executar com `/speckit.maintenance.run-tests`

Exemplos de Uso
Exemplo 1: Gerar testes para uma issue
Entrada:

```text
/speckit.maintenance.generate-tests issue https://github.com/rezluis/todo-app/issues/42
```
O que acontece:

1. Busca a issue #42 via MCP

2. Extrai os critérios de aceitação

3. Lê a constituição e os padrões de teste

4. Invoca test-generator.skill

5. Salva os testes em tests/

6. Apresenta o resumo

Exemplo 2: Gerar testes para um arquivo
Entrada:
```text
/speckit.maintenance.generate-tests file src/services/auth.service.ts
```

O que acontece:

1. Lê o arquivo e extrai sua interface pública (funções, classes, tipos)

2. Gera testes cobrindo cada função pública

3. Foca em comportamento esperado, não na implementação

Exemplo 3: Gerar testes para uma funcionalidade
Entrada:

```text
/speckit.maintenance.generate-tests feature "filtro de tarefas por status e prioridade"
```

O que acontece:

1. Usa a descrição como especificação

2. Gera testes cobrindo combinações de filtros

3. Salva em tests/integration/

### Tratamento de Erros[cite: 35]

| Erro | Ação |
| :--- | :--- |
| Issue não encontrada | Reportar erro e sugerir verificar a URL |
| Arquivo não existe | Reportar erro e listar arquivos similares |
| Framework de teste desconhecido | Perguntar ao usuário qual usar |
| Testes já existem | Perguntar se deve sobrescrever ou fazer merge |
| Sintaxe inválida | Corrigir automaticamente ou reportar |

### Boas Práticas[cite: 35]

* **Geração independente:** Nunca gerar testes a partir do corpo da implementação[cite: 35]
* **Foco no comportamento:** Testar o "o quê", não o "como"[cite: 35]
* **Cobertura progressiva:** Cobrir primeiro o cenário principal, depois casos de borda[cite: 35]
* **Seguir padrões:** Respeitar o estilo dos testes existentes no projeto[cite: 35]
* **Nomes descritivos:** Cada teste deve ser autoexplicativo pelo nome[cite: 35]



