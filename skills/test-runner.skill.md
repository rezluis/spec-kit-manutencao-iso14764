## Propósito

Esta skill executa os testes automatizados do projeto, captura os resultados (sucesso/falha), e em caso de falha, estrutura o feedback para que o `Implementer` possa corrigir sem criar uma nova issue.

## Entrada

```json
{
  "test_command": "npm test",
  "test_paths": [
    "tests/unit/auth.controller.test.ts",
    "tests/integration/auth.test.ts"
  ],
  "coverage_command": "npm test -- --coverage",
  "timeout_seconds": 300
}
```

### Etapa 1: Detectar o Comando de Teste[cite: 25]

Se `test_command` não foi fornecido, detectar automaticamente:[cite: 25]

| Linguagem | Comando |
| :--- | :--- |
| Node.js (Jest) | `npm test` ou `npx jest` |
| Python (Pytest) | `pytest` ou `python -m pytest` |
| Java (Maven) | `mvn test` |
| Java (Gradle) | `./gradlew test` |
| Go | `go test ./...` |
| Rust | `cargo test` |[cite: 25]

### Etapa 2: Executar os Testes[cite: 25]

1. Executar o comando no diretório do projeto[cite: 25]
2. Capturar stdout e stderr[cite: 25]
3. Respeitar timeout ( `timeout_seconds` )[cite: 25]

### Etapa 3: Parsear os Resultados[cite: 27]

Extrair do output:[cite: 27]

* Total de testes executados[cite: 27]
* Testes passados (quantidade)[cite: 27]
* Testes falhados (quantidade + lista)[cite: 27]
* Testes pulados (quantidade)[cite: 27]
* Tempo de execução[cite: 27]
* Para cada falha:[cite: 27]
  * Nome do teste[cite: 27]
  * Arquivo e linha[cite: 27]
  * Mensagem de erro[cite: 27]
  * Stack trace[cite: 27]
  * Assertions que falharam[cite: 27]

### Etapa 4: Verificar Cobertura (opcional)[cite: 27]

Se configurado, executar cobertura e verificar se atinge o mínimo definido na `constitution.md`.[cite: 27]

### Etapa 5: Determinar Resultado[cite: 27]

| Condição | Resultado |
| :--- | :--- |
| Todos os testes passam E cobertura OK | `success` |[cite: 27]
| Alguns testes falham | `failure` |[cite: 27]
| Cobertura abaixo do mínimo | `failure` |[cite: 27]
| Erro de compilação/sintaxe | `failure` |[cite: 27]
| Timeout | `failure` |[cite: 27]


Etapa 6: Estruturar Feedback (em caso de falha)
Se o resultado for `failure`, gerar um feedback estruturado para o `Implementer`:

```json

{
  "feedback": {
    "test_that_failed": "AuthController > login > should return 401 for invalid credentials",
    "file": "tests/unit/auth.controller.test.ts",
    "line": 42,
    "error_message": "Expected 401 but received 500",
    "expected": "401",
    "actual": "500",
    "stack_trace": "...",
    "hypothesis": "O tratamento de exceção não está capturando o erro antes de chegar ao middleware",
    "suggestion": "Verificar se o catch no AuthController está sendo executado ou se o erro está sendo re-lançado"
  }
}

```

Saída

Em caso de sucesso:

```json
{
  "status": "success",
  "summary": {
    "total": 15,
    "passed": 15,
    "failed": 0,
    "skipped": 0,
    "duration_seconds": 4.2
  },
  "coverage": {
    "lines": 82.5,
    "branches": 78.0,
    "functions": 85.0,
    "statements": 81.0,
    "meets_requirement": true
  },
  "next_action": "create_pull_request"
}
```
Em caso de falha:

```json
{
  "status": "failure",
  "summary": {
    "total": 15,
    "passed": 12,
    "failed": 3,
    "skipped": 0
  },
  "failures": [
    {
      "test": "should return 401 for invalid credentials",
      "file": "tests/unit/auth.controller.test.ts",
      "line": 42,
      "error": "Expected 401 but received 500",
      "expected": "401",
      "actual": "500",
      "hypothesis": "O tratamento de exceção não está capturando o erro",
      "suggestion": "Verificar se o catch no AuthController está sendo executado"
    }
  ],
  "raw_output": "string - output completo do teste",
  "next_action": "return_to_implementer"
}

```
Exemplo de Uso
Entrada:

```json
{"test_command": "npm test"}
```

```json
{
  "status": "success",
  "summary": {"total": 15, "passed": 15, "failed": 0},
  "next_action": "create_pull_request"
}
```
Saída (sucesso):

```json

{
  "status": "success",
  "summary": {"total": 15, "passed": 15, "failed": 0},
  "next_action": "create_pull_request"
}

```

Saída (falha):

```json
{
  "status": "failure",
  "failures": [
    {
      "test": "should return 401",
      "error": "Expected 401 but received 500",
      "hypothesis": "Exceção não capturada corretamente"
    }
  ],
  "next_action": "return_to_implementer"
}
```
### Tratamento de Erros[cite: 28]

| Erro | Ação |
| :--- | :--- |
| Comando não encontrado | Reportar e sugerir instalação[cite: 28] |
| Timeout | Matar processo e reportar[cite: 28] |
| Erro de compilação | Reportar como falha com foco no erro de sintaxe[cite: 28] |
| Dependências faltando | Sugerir instalação[cite: 28] |

### Boas Práticas[cite: 28]

* **Parseamento robusto:** Diferentes frameworks têm outputs diferentes[cite: 28]
* **Feedback acionável:** Cada falha deve ter hipótese e sugestão[cite: 28]
* **Preservar output bruto:** Salvar o output completo para debugging[cite: 28]
* **Limite de tentativas:** Se o Implementer falhar 3x seguidas, escalar para humano[cite: 28]


