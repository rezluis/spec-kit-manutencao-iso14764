---
description: "Gera testes automatizados após a correção ser aprovada pelo Reviewer"
---

## Propósito

Esta skill encapsula a geração de testes automatizados para uma mudança de manutenção já revisada e aprovada. Ela gera testes **unitários, de integração e de regressão** cobrindo o cenário da issue, casos de borda e funcionalidades existentes.

## Entrada

```json
{
  "issue": {
    "number": 42,
    "title": "string",
    "body": "string"
  },
  "changes_made": {
    "files_created": [{"path": "...", "summary": "..."}],
    "files_modified": [{"path": "...", "summary": "..."}]
  },
  "review_report": {
    "verdict": "approved",
    "issues_found": [...]
  },
  "project_context": {
    "language": "typescript",
    "framework": "express",
    "test_framework": "jest",
    "existing_tests_path": "tests/",
    "coverage_requirement": 80
  }
}

```

## Processo de Geração[cite: 21]

### Etapa 1: Identificar Cenários de Teste[cite: 21]

Com base na issue e nas mudanças feitas, listar os cenários:[cite: 21]

#### 1.1. Cenários da Issue (Happy Path)[cite: 21]

O cenário principal reportado na issue. Ex: "Login com credenciais inválidas retorna 401".[cite: 21]

#### 1.2. Cenários de Erro[cite: 21]

Casos de entrada inválida, exceções esperadas.[cite: 21]

#### 1.3. Cenários de Borda[cite: 21]

Limites: valores vazios, nulos, muito grandes, caracteres especiais.[cite: 21]

#### 1.4. Cenários de Regressão[cite: 21]

Funcionalidades existentes que não devem quebrar.[cite: 21]

### Etapa 2: Selecionar Tipos de Teste[cite: 21]

| Cenário | Tipo de Teste |
| :--- | :--- |
| Lógica isolada de função | Unitário |
| Interação entre módulos | Integração |
| Fluxo completo de usuário | E2E |
| Contrato de API | Contrato |
| Funcionalidade existente | Regressão |

### Etapa 3: Seguir Padrões do Projeto[cite: 22]

Ler os testes existentes em `tests/` para:[cite: 22]

* Descobrir o framework (Jest, Pytest, JUnit)[cite: 22]
* Descobrir a estrutura (describe/it, AAA, Given/When/Then)[cite: 22]
* Descobrir como mocks são criados[cite: 22]
* Descobrir como fixtures são geridos[cite: 22]
* Seguir a nomenclatura dos ficheiros ( `*.test.ts`, `test_*.py` )[cite: 22]

### Etapa 4: Gerar os Testes[cite: 22]

Para cada cenário, gerar:[cite: 22]

1. **Setup** — Mocks, fixtures, dados de entrada[cite: 22]
2. **Action** — Chamar a função/endpoint[cite: 22]
3. **Assertion** — Verificar o resultado esperado[cite: 22]
4. **Teardown** (se necessário)[cite: 22]

Estrutura sugerida (AAA - Arrange/Act/Assert):

```text

describe('AuthController.login', () => {
  // Arrange
  beforeEach(() => { /* setup */ });

  it('deve retornar 401 quando credenciais são inválidas', async () => {
    // Arrange
    const credentials = { email: 'user@example.com', password: 'wrong' };
    mockAuthService.login.mockRejectedValue(new UnauthorizedError());

    // Act
    await authController.login(mockReq, mockRes, mockNext);

    // Assert
    expect(mockRes.status).toHaveBeenCalledWith(401);
    expect(mockRes.json).toHaveBeenCalledWith({ error: 'Invalid credentials' });
  });

  it('deve retornar 200 quando credenciais são válidas', async () => {
    // ... teste de regressão
  });
});

```
### Etapa 5: Verificar Cobertura[cite: 23]

Para cada arquivo modificado, garantir que os testes cobrem:[cite: 23]

* [ ] Linhas novas adicionadas[cite: 23]
* [ ] Branches condicionais (if/else, switch)[cite: 23]
* [ ] Exceções lançadas[cite: 23]
* [ ] Casos de borda[cite: 23]

### Etapa 6: Validar Sintaxe[cite: 23]

Antes de salvar, verificar que os testes:[cite: 23]

* Compilam (para linguagens tipadas)[cite: 23]
* Têm imports corretos[cite: 23]
* Referenciam arquivos existentes[cite: 23]

Saida:

```json
{
  "status": "success",
  "tests_created": [
    {
      "path": "tests/unit/auth.controller.test.ts",
      "test_cases": 3,
      "scenarios": ["happy_path", "invalid_credentials", "missing_fields"],
      "type": "unit"
    },
    {
      "path": "tests/integration/auth.test.ts",
      "test_cases": 2,
      "scenarios": ["full_login_flow", "regression"],
      "type": "integration"
    }
  ],
  "coverage_estimate": "+3.2%",
  "notes": [
    "3 testes unitários para o AuthController",
    "2 testes de integração para o fluxo de login"
  ]
}

```
Exemplo de uso

Entrada:

```json

{
  "issue": {"number": 42, "title": "Erro 500 no login"},
  "changes_made": {
    "files_modified": [
      {"path": "src/controllers/auth.controller.ts", "summary": "Retorna 401"}
    ]
  },
  "project_context": {"test_framework": "jest"}
}

```
Saida:

```json
{
  "status": "success",
  "tests_created": [
    {
      "path": "tests/unit/auth.controller.test.ts",
      "test_cases": 3,
      "type": "unit"
    }
  ]
}

```
### Tratamento de Erros[cite: 24]

| Erro | Ação |
| :--- | :--- |
| Framework de teste desconhecido | Perguntar ao usuário[cite: 24] |
| Arquivo de teste já existe | Perguntar se deve sobrescrever ou criar novo[cite: 24] |
| Código não compila | Reportar erro com detalhes[cite: 24] |

### Boas Práticas[cite: 24]

* **Cobrir o cenário da issue primeiro:** O teste principal é o que valida a correção[cite: 24]
* **Adicionar testes de regressão:** Garantir que nada quebrou[cite: 24]
* **Seguir o padrão do projeto:** Não introduzir frameworks ou estilos novos[cite: 24]
* **Não gerar testes triviais:** Evitar testes que sempre passam[cite: 24]
* **Testar comportamento, não implementação:** Focar no "o quê", não no "como"[cite: 24]


