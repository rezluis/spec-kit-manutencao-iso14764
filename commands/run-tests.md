---
description: "Executa a suíte de testes do projeto e apresenta os resultados"
---

# Comando: Rodar Testes

Executa a suíte de testes automatizados do projeto, com suporte a escopos (todos, arquivo específico, apenas unitários, apenas integração) e apresentação estruturada dos resultados.

## Entrada do Usuário
$ARGUMENTS

## Modos de Uso

### Modo 1: Rodar Toda a Suíte

/speckit.maintenance.run-tests


### Modo 2: Rodar Apenas um Arquivo

/speckit.maintenance.run-tests tests/unit/auth.controller.test.ts


### Modo 3: Rodar Apenas uma Categoria

/speckit.maintenance.run-tests --unit
/speckit.maintenance.run-tests --integration
/speckit.maintenance.run-tests --e2e


### Modo 4: Rodar com Cobertura

/speckit.maintenance.run-tests --coverage


### Modo 5: Rodar Apenas Testes que Falharam Anteriormente

/speckit.maintenance.run-tests --failed


## Processo de Execução

### Etapa 1: Detectar o Framework de Teste

Se o framework não estiver explícito na `constitution.md`, detectar automaticamente:

| Arquivo Encontrado | Framework Provável | Comando |
|:---|:---|:---|
| `package.json` + `jest.config.js` | Jest | `npm test` |
| `package.json` + `vitest.config.ts` | Vitest | `npm test` |
| `pytest.ini` ou `pyproject.toml` | Pytest | `pytest` |
| `pom.xml` | Maven (JUnit) | `mvn test` |
| `build.gradle` | Gradle | `./gradlew test` |
| `go.mod` | Go | `go test ./...` |
| `Cargo.toml` | Rust | `cargo test` |

### Etapa 2: Interpretar o Escopo

Com base em `$ARGUMENTS`:

- **Vazio:** Rodar toda a suíte
- **Caminho de arquivo:** Rodar apenas aquele arquivo
- **`--unit`:** Rodar apenas testes unitários (`tests/unit/`)
- **`--integration`:** Rodar apenas testes de integração (`tests/integration/`)
- **`--e2e`:** Rodar apenas testes end-to-end (`tests/e2e/`)
- **`--coverage`:** Adicionar flag de cobertura
- **`--failed`:** Rodar apenas testes que falharam na última execução

### Etapa 3: Executar os Testes

Invocar a skill `test-runner`:

```text
call skill test-runner
test_command={comando detectado}
test_paths={caminhos ou null}
coverage_command={comando com --coverage ou null}
timeout_seconds=300
```


A skill executará os testes, parseará o output e retornará o resultado estruturado.

### Etapa 4: Apresentar os Resultados

#### Em caso de sucesso:

## ✅ Testes Passando

### Resumo
- **Total:** 47 testes
- **Passados:** 47 ✅
- **Falhados:** 0
- **Pulados:** 0
- **Tempo:** 4.2s

### Cobertura
- Linhas: 82.5% (meta: 80% ✅)
- Branches: 78.0%
- Funções: 85.0%
- Statements: 81.0%

### Próximos Passos
- Código está saudável
- Nenhuma ação necessária

Em caso de falha:

## ❌ Testes Falhando

### Resumo
- **Total:** 47 testes
- **Passados:** 44 ✅
- **Falhados:** 3 ❌
- **Tempo:** 5.1s

### Falhas Detectadas

#### 1. `AuthController > login > should return 401 for invalid credentials`
- **Arquivo:** `tests/unit/auth.controller.test.ts:42`
- **Erro:** `Expected 401 but received 500`
- **Esperado:** `401`
- **Obtido:** `500`
- **Hipótese:** O tratamento de exceção não está capturando o erro antes do middleware

#### 2. `TaskService > create > should reject empty title`
- **Arquivo:** `tests/unit/task.service.test.ts:78`
- **Erro:** `Expected ValidationError but received null`

#### 3. `Integration > POST /tasks > returns 201 for valid payload`
- **Arquivo:** `tests/integration/tasks.test.ts:23`
- **Erro:** Timeout após 5000ms

### Opções de Ação

1. **Corrigir automaticamente** — invocar `/speckit.maintenance.implement` com o feedback
2. **Ver detalhes** — mostrar output bruto de um teste específico
3. **Ignorar** — prosseguir mesmo com falhas (não recomendado)
4. **Cancelar** — encerrar sem ação

### Etapa 5: Registrar Histórico
Salvar o resultado em .specify/maintenance/test-results/run-{YYYY-MM-DD-HHMMSS}.json para consulta futura.

Exemplos de Uso
Exemplo 1: Rodar tudo
Entrada:

```text
/speckit.maintenance.run-tests
```

Saída: resumo completo com todos os testes.

Exemplo 2: Rodar apenas testes unitários com cobertura
Entrada:

```text
/speckit.maintenance.run-tests --unit --coverage
```

Saída: resumo filtrado + cobertura.

Exemplo 3: Rodar apenas um arquivo
Entrada:

```text
/speckit.maintenance.run-tests tests/unit/auth.controller.test.ts
```

Saída: resultado apenas daquele arquivo.

Exemplo 4: Rodar apenas testes que falharam
Entrada:

```text
/speckit.maintenance.run-tests --failed
```

Saída: apenas os testes que falharam na execução anterior.

### Tratamento de Erros[cite: 36]

| Erro | Ação |
| :--- | :--- |
| Nenhum framework detectado | Perguntar ao usuário qual comando rodar[cite: 36] |
| Comando de teste inválido | Reportar erro e sugerir correção[cite: 36] |
| Timeout | Matar processo e reportar testes que travaram[cite: 36] |
| Erro de compilação | Reportar como falha com foco no erro de sintaxe[cite: 36] |
| Dependências faltando | Sugerir `npm install` ou equivalente[cite: 36] |

### Boas Práticas[cite: 36]

* **Apresentação clara:** Sempre mostrar resumo antes dos detalhes[cite: 36]
* **Foco em ação:** Cada falha deve ter hipótese e sugestão[cite: 36]
* **Preservar output bruto:** Salvar em arquivo para debugging posterior[cite: 36]
* **Rápido por padrão:** Sem `--coverage` a menos que solicitado (cobertura é lenta)[cite: 36]
* **Feedback acionável:** Em caso de falha, oferecer o próximo passo concreto[cite: 36]


