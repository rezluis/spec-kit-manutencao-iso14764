---
description: "Gera o código da mudança de manutenção seguindo os padrões do projeto"
---

## Propósito
Esta skill encapsula a lógica de geração de código para uma mudança de manutenção. Ela recebe o plano de implementação (do relatório de impacto), lê a `constitution.md` do projeto, e gera o código respeitando os padrões, arquitetura e convenções definidos.

## Entrada

```json
{
  "issue": {
    "number": 42,
    "title": "string",
    "body": "string"
  },
  "classification": {
    "type": "corretiva|adaptativa|perfectiva|preventiva",
    "urgency": "alta|media|baixa"
  },
  "affected_modules": [
    {
      "name": "AuthController",
      "type": "controller",
      "impact_level": "alto",
      "reason": "string"
    }
  ],
  "approach": "string - abordagem sugerida pelo Impact Analyst",
  "project_context": {
    "language": "typescript|python|java|...",
    "framework": "express|django|spring|...",
    "constitution_path": ".specify/memory/constitution.md",
    "rules_path": ".specify/rules/",
    "test_framework": "jest|pytest|junit|...",
    "file_structure": "opcional - estrutura de diretórios"
  }
}

```

**Processo de Geração de Código**

**Etapa 1: Carregar Contexto Obrigatório**

Antes de gerar qualquer código, ler obrigatoriamente:

1. `constitution.md` em `.specify/memory/constitution.md` para conhecer:
   * Linguagem e versão
   * Framework e bibliotecas obrigatórias
   * Padrões de código (estilo, nomenclatura, formatação)
   * Arquitetura obrigatória (camadas, padrões)
   * Políticas de segurança
   * Convenções de testes
2. `rules/coding-standards.rules.md` para conhecer:
   * Convenções específicas de nomenclatura
   * Padrões de organização de arquivos
   * Regras de importação/exportação
   * Padrões de tratamento de erros
3. `rules/iso-14764.rules.md` para conhecer:
   * Regras específicas de manutenção
   * Requisitos de rastreabilidade
   * Padrões de documentação de mudanças
4. **Arquivos existentes** dos módulos afetados para entender:
   * Estilo de código atual
   * Padrões de implementação
   * Bibliotecas utilizadas
   * Estrutura de classes/funções

**Regra crítica:** Se houver conflito entre o que foi sugerido no relatório de impacto e o que está na `constitution.md`, a `constitution.md` **sempre prevalece**. Neste caso, notificar o usuário sobre o conflito.

**Etapa 2: Validar a Abordagem**

Antes de gerar o código, verificar:

1. **A abordagem sugerida é viável** dentro das restrições da `constitution.md`?
2. **Existem bibliotecas/padrões** no projeto que podem ser reutilizados?
3. **A abordagem respeita** as camadas arquiteturais definidas?
4. **Há necessidade de refatoração** além do escopo original?

Se a resposta a alguma dessas perguntas for negativa, propor uma alternativa alinhada à `constitution.md` e documentar a decisão.

**Etapa 3: Planejar a Geração por Módulo**

Para cada módulo afetado, planejar:

1. **Tipo de mudança:**
   * **Criação:** Novo arquivo/módulo
   * **Modificação:** Alteração em arquivo existente
   * **Remoção:** Exclusão de arquivo/módulo
2. **Estrutura do código:**
   * Classes/funções a criar ou modificar
   * Imports necessários
   * Tipos/interfaces a definir
   * Constantes e configurações
3. **Ordem de geração:**
   * Começar pelas dependências (tipos, interfaces, utils)
   * Depois pelas camadas de domínio (models, services)
   * Por último pelas camadas de aplicação (controllers, rotas)

**Etapa 4: Gerar o Código**

**4.1. Regras Gerais de Geração**

* **Seguir a linguagem e versão** definidas na `constitution.md`
* **Usar as bibliotecas** já presentes no projeto (não introduzir novas sem justificativa)
* **Respeitar a arquitetura em camadas** (controllers $\rightarrow$ services $\rightarrow$ repositories)
* **Aplicar os padrões de nomenclatura** do projeto (camelCase, snake_case, PascalCase)
* **Incluir tipagem** quando a linguagem suportar (TypeScript, Python types, etc.)
* **Adicionar comentários** apenas quando a lógica não for autoexplicativa
* **Tratar erros** de forma consistente com o restante do projeto

**4.2. Regras Específicas por Tipo de Manutenção**

**Corretiva:**

* Mudanças **mínimas e cirúrgicas**
* Preservar o comportamento existente que não deve ser alterado
* Adicionar tratamento de erro específico para o caso reportado
* Não refatorar código ao redor (a menos que estritamente necessário)

**Adaptativa:**

* Atualizar dependências e configurações
* Verificar compatibilidade de APIs
* Adaptar chamadas para novas versões de bibliotecas
* Atualizar testes que dependem da versão antiga

**Perfectiva:**

* Focar na melhoria solicitada (performance, usabilidade, etc.)
* Manter comportamento externo idêntico (a menos que explicitamente alterado)
* Adicionar benchmarks/métricas se aplicável
* Documentar a melhoria com comentários

**Preventiva:**

* Aplicar correções de segurança ou robustez
* Adicionar validações e verificações
* Atualizar dependências vulneráveis
* Documentar o risco mitigado

**4.3. Estrutura de Cada Arquivo Gerado**

Cada arquivo gerado deve seguir esta estrutura:

```text
1. Imports (agrupados por origem: externos, internos, tipos)
2. Constantes e configurações
3. Tipos e interfaces
4. Funções/classes principais
5. Funções/classes auxiliares
6. Exports

```

**4.4. Exemplo de Geração**

**Contexto:**

* **Linguagem:** TypeScript
* **Framework:** Express
* **Padrão:** Clean Architecture
* **Módulo afetado:** `AuthController`

**Código gerado (modificação):**

```text
// src/controllers/auth.controller.ts
import { Request, Response, NextFunction } from 'express';
import { AuthService } from '../services/auth.service';
import { LoginDTO } from '../dtos/auth.dto';
import { UnauthorizedError } from '../errors/unauthorized.error';
import { ValidationError } from '../errors/validation.error';

export class AuthController {
  constructor(private authService: AuthService) {}

  async login(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const credentials: LoginDTO = req.body;
      
      // Validação básica
      if (!credentials.email || !credentials.password) {
        throw new ValidationError('Email and password are required');
      }

      const result = await this.authService.login(credentials);
      res.status(200).json(result);
    } catch (error) {
      // Correção: retorna 401 para credenciais inválidas em vez de propagar erro 500
      if (error instanceof UnauthorizedError) {
        res.status(401).json({ error: 'Invalid credentials' });
        return;
      }
      
      next(error);
    }
  }
}
```

**Etapa 5: Gerar Testes Associados**

Para cada módulo modificado, gerar testes que:

1. **Cubram o cenário reportado** na issue (para corretivas)
2. **Cubram cenários de sucesso e erro**
3. **Cubram edge cases** identificados no relatório de impacto
4. **Garantam que funcionalidades existentes** continuam funcionando (regressão)

**Estrutura de testes:**

```text

1. Setup (mocks, fixtures, configuração)
2. Testes do cenário principal (o que motivou a mudança)
3. Testes de cenários alternativos
4. Testes de edge cases
5. Testes de regressão

```

**Exemplo de teste gerado:**

```text

// tests/unit/auth.controller.test.ts
import { AuthController } from '../../src/controllers/auth.controller';
import { AuthService } from '../../src/services/auth.service';
import { UnauthorizedError } from '../../src/errors/unauthorized.error';

describe('AuthController', () => {
  let authController: AuthController;
  let mockAuthService: jest.Mocked<AuthService>;
  let mockReq: any;
  let mockRes: any;
  let mockNext: jest.Mock;

  beforeEach(() => {
    mockAuthService = {
      login: jest.fn(),
    } as any;
    
    authController = new AuthController(mockAuthService);
    
    mockReq = { body: {} };
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn(),
    };
    mockNext = jest.fn();
  });

  describe('login', () => {
    it('should return 200 with token for valid credentials', async () => {
      mockReq.body = { email: 'test@example.com', password: 'password123' };
      mockAuthService.login.mockResolvedValue({
        token: 'valid-token',
        user: { id: '1', email: 'test@example.com' },
      });

      await authController.login(mockReq, mockRes, mockNext);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({
        token: 'valid-token',
        user: expect.any(Object),
      });
    });

    it('should return 401 for invalid credentials', async () => {
      mockReq.body = { email: 'test@example.com', password: 'wrong' };
      mockAuthService.login.mockRejectedValue(new UnauthorizedError());

      await authController.login(mockReq, mockRes, mockNext);

      expect(mockRes.status).toHaveBeenCalledWith(401);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'Invalid credentials' });
      expect(mockNext).not.toHaveBeenCalled();
    });

    it('should return 400 when email or password is missing', async () => {
      mockReq.body = { email: 'test@example.com' };

      await authController.login(mockReq, mockRes, mockNext);

      expect(mockRes.status).toHaveBeenCalledWith(400);
    });
  });
});

```

**Etapa 6: Atualizar Documentação**

Se a mudança impactar documentação:

* **Comentários JSDoc/Docstring** para funções/métodos públicos
* **README.md** se houver mudança de comportamento visível
* **API docs** (Swagger/OpenAPI) se houver mudança em endpoints
* **CHANGELOG.md** com entrada descrevendo a mudança

**Etapa 7: Validar o Código Gerado**

Antes de retornar, validar:

1. **Sintaxe:** O código compila sem erros?
2. **Tipagem:** Os tipos estão corretos? (para linguagens tipadas)
3. **Linter:** O código passa no linter do projeto?
4. **Testes:** Os testes gerados passam?
5. **Consistência:** O código segue os padrões do projeto?
6. **Escopo:** O código está limitado ao escopo do relatório de impacto?

Se alguma validação falhar, corrigir e repetir.

**Saída**

A skill deve retornar um objeto JSON com a seguinte estrutura:

```json

{
  "status": "success|partial|failed",
  "files_created": [
    {
      "path": "src/controllers/auth.controller.ts",
      "type": "modification",
      "lines_added": 15,
      "lines_removed": 5,
      "summary": "Adiciona tratamento específico para UnauthorizedError"
    }
  ],
  "files_modified": [
    {
      "path": "src/services/auth.service.ts",
      "type": "modification",
      "lines_added": 8,
      "lines_removed": 2,
      "summary": "Lança UnauthorizedError em vez de Error genérico"
    }
  ],
  "tests_created": [
    {
      "path": "tests/unit/auth.controller.test.ts",
      "test_cases": 3,
      "summary": "Cobre cenários de sucesso, credenciais inválidas e validação"
    }
  ],
  "docs_updated": [
    {
      "path": "CHANGELOG.md",
      "summary": "Adiciona entrada para correção de erro 500 no login"
    }
  ],
  "validation": {
    "syntax_ok": true,
    "types_ok": true,
    "lint_ok": true,
    "tests_passing": true,
    "coverage_impact": "+2.5%"
  },
  "notes": [
    "Não foi necessário refatorar o AuthService, apenas ajustar o tipo de erro lançado"
  ],
  "warnings": [
    "Considere adicionar rate limiting no endpoint de login em uma próxima iteração"
  ]
}

```

**Exemplos de Uso**

**Exemplo 1: Geração para Correção de Bug (Corretiva)**

Entrada:

```json

{
  "issue": {"number": 42, "title": "Erro 500 no login"},
  "classification": {"type": "corretiva", "urgency": "alta"},
  "affected_modules": [{"name": "AuthController", "impact_level": "alto"}],
  "approach": "Correção direta no tratamento de exceções",
  "project_context": {
    "language": "typescript",
    "framework": "express",
    "test_framework": "jest"
  }
}

```

Saida(resumida):

```json

{
  "status": "success",
  "files_modified": [
    {
      "path": "src/controllers/auth.controller.ts",
      "summary": "Adiciona try/catch para UnauthorizedError e retorna 401"
    }
  ],
  "tests_created": [
    {
      "path": "tests/unit/auth.controller.test.ts",
      "test_cases": 3
    }
  ],
  "validation": {
    "syntax_ok": true,
    "tests_passing": true
  }
}

```

**Exemplo 2: Geração para Atualização de Dependência (Adaptativa)**

Entrada:

```json
{
  "issue": {"number": 55, "title": "Atualizar Express 4 para 5"},
  "classification": {"type": "adaptativa", "urgency": "media"},
  "affected_modules": [{"name": "server.ts", "impact_level": "alto"}],
  "approach": "Atualizar dependência e adaptar middlewares",
  "project_context": {
    "language": "typescript",
    "framework": "express"
  }
}

```

Saida(resumida):

```json

{
  "status": "success",
  "files_modified": [
    {
      "path": "package.json",
      "summary": "Atualiza express de ^4.18.0 para ^5.0.0"
    },
    {
      "path": "src/server.ts",
      "summary": "Adapta middlewares para API do Express 5"
    }
  ],
  "tests_created": [
    {
      "path": "tests/integration/server.test.ts",
      "test_cases": 5
    }
  ],
  "validation": {
    "tests_passing": true
  },
  "notes": [
    "A API de middlewares assíncronos mudou no Express 5; ajustes aplicados"
  ]
}

```

**Tratamento de Erros**

| Erro | Ação |
| :--- | :--- |
| **Conflito com constitution.md** | Retornar `status: "partial"`, notificar conflito e propor alternativa |
| **Arquivo não encontrado** | Verificar caminhos, tentar variações, se falhar retornar erro |
| **Linguagem/framework desconhecido** | Solicitar mais contexto ao usuário |
| **Testes falhando após geração** | Corrigir automaticamente se possível; senão retornar `status: "partial"` |
| **Lint falhando** | Corrigir automaticamente (formatação, imports) |
| **Dependência nova necessária** | Verificar se está na constitution.md; se não, alertar o usuário |

**Boas Práticas**

* **Menos é mais:** Prefira mudanças pequenas e cirúrgicas a grandes refatorações
* **Reutilize:** Sempre prefira reutilizar código existente a criar novo
* **Consistência:** O código gerado deve parecer ter sido escrito pelo time do projeto
* **Rastreabilidade:** Comente decisões não óbvias com referência à issue
* **Validação:** Nunca retorne código sem ter validado sintaxe e testes
* **Transparência:** Documente o que foi feito, por que, e o que ficou de fora
* **Segurança:** Nunca introduza padrões inseguros, mesmo que sejam "mais rápidos"