---
description: "Avalia o impacto técnico de uma mudança de manutenção no sistema"
---

## Propósito
Esta skill analisa os dados de uma issue de manutenção (já classificada) e avalia seu impacto técnico no sistema, identificando módulos afetados, estimando esforço, avaliando riscos e gerando recomendações acionáveis para implementação.

## Entrada

```json
{
  "issue": {
    "number": 42,
    "title": "string",
    "body": "string",
    "labels": ["string"],
    "comments": [{"user": "string", "body": "string"}]
  },
  "classification": {
    "type": "corretiva|adaptativa|perfectiva|preventiva",
    "confidence": "alta|media|baixa",
    "justification": "string",
    "urgency": "alta|media|baixa"
  },
  "project_context": {
    "repository": "string",
    "branch": "string",
    "structure": "opcional - lista de módulos/arquivos se disponível"
  }
}

```

# Processo de Avaliação

## Etapa 1: Identificação de Módulos Afetados

### 1.1. Análise do Texto da Issue

1. Extrair menções diretas a módulos, arquivos, classes ou funções no texto da issue.
2. Identificar termos técnicos que indiquem componentes (ex: `AuthController`, `UserService`, `database`, `API`).
3. Analisar comentários em busca de referências a locais específicos do código.

### 1.2. Análise do Contexto do Projeto

Se `project_context.structure` estiver disponível:

1. Mapear os módulos mencionados na issue para a estrutura real do projeto.
2. Identificar módulos relacionados (por nome similar ou por dependência).
3. Detectar módulos de infraestrutura que podem ser afetados indiretamente.

### 1.3. Classificação do Nível de Impacto por Módulo

# Etapa 2: Estimativa de Esforço

Avaliar o esforço com base em múltiplos fatores:

## 2.1. Fatores de Complexidade

| Fator | Baixa (1) | Média (2) | Alta (3) |
|---|---|---|---|
| Número de módulos afetados | 1 | 2-3 | 4+ |
| Nível de impacto | Apenas Baixo | Até Médio | Pelo menos um Alto |
| Dependências afetadas | Nenhuma | 1-2 | 3+ |
| Necessidade de testes novos | Nenhum | Alguns | Muitos |
| Risco de regressão | Baixo | Médio | Alto |

## 2.2. Cálculo da Estimativa

Calcular a pontuação total e mapear para uma estimativa:

| Pontuação | Tamanho | Dias Estimados |
|---|---|---|
| 5-7 | Pequeno | 0.5 - 2 dias |
| 8-10 | Médio | 3 - 5 dias |
| 11-13 | Grande | 1 - 2 semanas |
| 14-15 | Muito Grande | > 2 semanas |

# Etapa 3: Avaliação de Riscos

Identificar e classificar riscos em três categorias:

## 3.1. Risco Técnico

- **Falhas na implementação:** Complexidade do código afetado
- **Regressões:** Módulos com pouca cobertura de testes
- **Quebra de dependências:** Interfaces públicas que podem mudar
- **Compatibilidade:** Mudanças que afetam outras partes do sistema

### Classificação:

- **Alto:** Módulos críticos sem testes, interfaces públicas afetadas
- **Médio:** Módulos com testes parciais, dependências controladas
- **Baixo:** Mudança isolada, cobertura de testes adequada

## 3.2. Risco de Prazo

- **Dependências externas:** Bibliotecas, APIs de terceiros
- **Bloqueios:** Necessidade de aprovação, dependência de outros times
- **Complexidade subestimada:** Baseada na análise inicial

## 3.3. Risco de Negócio

- **Impacto em funcionalidades críticas:** Fluxos essenciais do sistema
- **Indisponibilidade:** Necessidade de downtime ou janela de manutenção
- **Experiência do usuário:** Mudanças visíveis para o usuário final

# Etapa 4: Geração de Recomendações

## 4.1. Abordagem Sugerida

Com base no tipo de manutenção e nos módulos afetados, sugerir uma das seguintes abordagens:

- **Correção direta:** Ajuste pontual no código, sem refatoração
- **Correção com refatoração:** Ajuste + melhoria do código ao redor
- **Refatoração gradual:** Melhoria incremental com testes contínuos
- **Workaround temporário:** Solução paliativa enquanto a definitiva é planejada
- **Reescrita do módulo:** Quando a complexidade justifica uma reescrita

## 4.2. Estratégia de Testes

Recomendar os tipos de teste necessários:

- **Testes unitários:** Para funções/métodos modificados
- **Testes de integração:** Para interações entre módulos afetados
- **Testes de regressão:** Para garantir que funcionalidades existentes continuam funcionando
- **Testes de contrato:** Se houver mudança em interfaces públicas
- **Testes end-to-end:** Para fluxos de usuário afetados

## 4.3. Plano de Rollback

Sugerir estratégias de reversão:

- **Feature flag:** Se a mudança pode ser isolada por flag
- **Revert de commit:** Se a mudança é pequena e isolada
- **Deploy anterior:** Se a mudança é em ambiente com versionamento
- **Backup de dados:** Se a mudança envolve migração de dados

## 4.4. Prioridade e Sequenciamento

Recomendar prioridade com base em:

- Urgência da classificação
- Impacto no negócio
- Risco técnico
- Dependências com outras tarefas

**Etapa 5: Geração do Relatório de Impacto**

Estruturar o resultado em um objeto JSON:

```json

{
  "affected_modules": [
    {
      "name": "string",
      "type": "controller|service|repository|model|middleware|config|other",
      "impact_level": "alto|medio|baixo",
      "reason": "string",
      "is_public_interface": true
    }
  ],
  "effort_estimate": {
    "size": "pequeno|medio|grande|muito_grande",
    "days_min": 0.5,
    "days_max": 2,
    "complexity_score": 7,
    "complexity_factors": ["fator1", "fator2"]
  },
  "risks": {
    "technical": [
      {
        "description": "string",
        "probability": "alta|media|baixa",
        "impact": "alto|medio|baixo",
        "mitigation": "string"
      }
    ],
    "schedule": [
      {
        "description": "string",
        "probability": "alta|media|baixa",
        "impact": "alto|medio|baixo",
        "mitigation": "string"
      }
    ],
    "business": [
      {
        "description": "string",
        "probability": "alta|media|baixa",
        "impact": "alto|medio|baixo",
        "mitigation": "string"
      }
    ]
  },
  "recommendations": {
    "approach": "string",
    "testing_strategy": ["string"],
    "rollback_plan": "string",
    "priority": "alta|media|baixa",
    "next_steps": ["string"]
  },
  "dependencies": {
    "internal_modules": ["string"],
    "external_packages": ["string"],
    "other_tasks": ["string"]
  },
  "summary": "string"
}

```

**Exemplo de Uso**

Exemplo 1: Manutenção Corretiva Simples

Entrada:

```json

{
  "issue": {
    "number": 42,
    "title": "Erro ao fazer login com credenciais inválidas",
    "body": "Quando o usuário fornece credenciais inválidas, o sistema retorna erro 500 em vez de 401.",
    "labels": ["bug", "security"],
    "comments": [
      {"user": "dev1", "body": "O erro ocorre no AuthController, linha 42"}
    ]
  },
  "classification": {
    "type": "corretiva",
    "confidence": "alta",
    "justification": "Comportamento incorreto do sistema",
    "urgency": "alta"
  }
}

```

Saida:

```json

{
  "affected_modules": [
    {
      "name": "AuthController",
      "type": "controller",
      "impact_level": "alto",
      "reason": "Contém a lógica de tratamento de login que precisa ser ajustada",
      "is_public_interface": true
    },
    {
      "name": "AuthService",
      "type": "service",
      "impact_level": "medio",
      "reason": "Pode precisar ajustar o retorno de erros para o controller",
      "is_public_interface": false
    },
    {
      "name": "ErrorMiddleware",
      "type": "middleware",
      "impact_level": "baixo",
      "reason": "Verificar se está capturando corretamente as exceções",
      "is_public_interface": false
    }
  ],
  "effort_estimate": {
    "size": "pequeno",
    "days_min": 0.5,
    "days_max": 1,
    "complexity_score": 6,
    "complexity_factors": [
      "Apenas 1 módulo com impacto alto",
      "Sem dependências externas afetadas",
      "Testes unitários existentes para o módulo"
    ]
  },
  "risks": {
    "technical": [
      {
        "description": "Regressão em outros fluxos de autenticação",
        "probability": "baixa",
        "impact": "medio",
        "mitigation": "Executar testes de integração de autenticação após a mudança"
      }
    ],
    "schedule": [],
    "business": [
      {
        "description": "Exposição de informações internas se o tratamento de erros for mal feito",
        "probability": "media",
        "impact": "alto",
        "mitigation": "Revisar mensagens de erro para não expor detalhes internos"
      }
    ]
  },
  "recommendations": {
    "approach": "Correção direta: ajustar o tratamento de exceções no AuthController para capturar erros específicos e retornar 401 em vez de propagar o erro",
    "testing_strategy": [
      "Teste unitário para o AuthController com credenciais inválidas",
      "Teste de integração para o fluxo completo de login"
    ],
    "rollback_plan": "Revert de commit (mudança pequena e isolada)",
    "priority": "alta",
    "next_steps": [
      "Criar branch fix/login-error-handling",
      "Ajustar o AuthController",
      "Escrever testes para cenários de credenciais inválidas",
      "Executar testes de regressão",
      "Validar em ambiente de desenvolvimento"
    ]
  },
  "dependencies": {
    "internal_modules": ["UserRepository", "TokenService"],
    "external_packages": [],
    "other_tasks": []
  },
  "summary": "Manutenção corretiva de baixo esforço (0.5-1 dia) focada no AuthController. Risco técnico baixo, mas risco de negócio médio devido à exposição de informações. Prioridade alta por envolver segurança."
}

```

Exemplo 2: Manutenção Adaptativa de Médio Porte

Entrada:

```json

{
  "issue": {
    "number": 55,
    "title": "Atualizar Node.js 18 para 20 LTS",
    "body": "O Node.js 18 está em fim de vida. Precisamos atualizar para a versão 20 LTS para manter suporte e segurança.",
    "labels": ["dependencies", "upgrade"],
    "comments": [
      {"user": "dev1", "body": "É preciso verificar compatibilidade com as bibliotecas"},
      {"user": "dev2", "body": "Já testei localmente e parece funcionar"}
    ]
  },
  "classification": {
    "type": "adaptativa",
    "confidence": "alta",
    "justification": "Adaptação ao fim de vida do Node.js 18",
    "urgency": "media"
  }
}

```

Saida:

```json

{
  "affected_modules": [
    {
      "name": "package.json",
      "type": "config",
      "impact_level": "alto",
      "reason": "Contém a versão do Node.js e dependências que precisam ser atualizadas",
      "is_public_interface": false
    },
    {
      "name": "Dockerfile",
      "type": "config",
      "impact_level": "alto",
      "reason": "Define a imagem base do Node.js utilizada no deploy",
      "is_public_interface": false
    },
    {
      "name": "CI/CD workflows",
      "type": "config",
      "impact_level": "medio",
      "reason": "Precisa ser atualizado para usar a versão 20 do Node.js",
      "is_public_interface": false
    },
    {
      "name": "src/**",
      "type": "other",
      "impact_level": "medio",
      "reason": "Pode haver incompatibilidades com a nova versão do Node.js",
      "is_public_interface": false
    }
  ],
  "effort_estimate": {
    "size": "medio",
    "days_min": 3,
    "days_max": 5,
    "complexity_score": 9,
    "complexity_factors": [
      "Múltiplos módulos de configuração afetados",
      "Necessidade de verificar compatibilidade de bibliotecas",
      "Potencial impacto em todo o código-fonte"
    ]
  },
  "risks": {
    "technical": [
      {
        "description": "Incompatibilidade de bibliotecas com Node.js 20",
        "probability": "media",
        "impact": "alto",
        "mitigation": "Executar todos os testes automatizados após a atualização"
      },
      {
        "description": "Mudança de comportamento em APIs deprecadas",
        "probability": "media",
        "impact": "medio",
        "mitigation": "Revisar changelog do Node.js e buscar por APIs deprecadas"
      }
    ],
    "schedule": [
      {
        "description": "Tempo para validação completa em ambiente de staging",
        "probability": "media",
        "impact": "medio",
        "mitigation": "Reservar janela de tempo para testes em staging"
      }
    ],
    "business": [
      {
        "description": "Possível indisponibilidade durante o deploy",
        "probability": "baixa",
        "impact": "medio",
        "mitigation": "Realizar deploy em janela de manutenção programada"
      }
    ]
  },
  "recommendations": {
    "approach": "Refatoração gradual: atualizar a versão do Node.js primeiro em ambiente de desenvolvimento, depois staging, e finalmente produção. Corrigir incompatibilidades conforme apareçam.",
    "testing_strategy": [
      "Executar suíte completa de testes automatizados",
      "Teste de fumaça em staging antes de ir para produção",
      "Monitoramento intensivo pós-deploy"
    ],
    "rollback_plan": "Feature flag + deploy anterior: manter a versão anterior disponível para rollback rápido",
    "priority": "media",
    "next_steps": [
      "Atualizar package.json e Dockerfile",
      "Atualizar workflows de CI/CD",
      "Executar testes localmente",
      "Validar em staging",
      "Agendar deploy em produção"
    ]
  },
  "dependencies": {
    "internal_modules": [],
    "external_packages": [
      "Express", "Prisma", "Jest", "todas as dependências do package.json"
    ],
    "other_tasks": [
      "Atualizar documentação de requisitos de ambiente"
    ]
  },
  "summary": "Manutenção adaptativa de médio porte (3-5 dias) que afeta principalmente configurações e potencialmente todo o código-fonte. Risco técnico médio-alto devido a incompatibilidades de bibliotecas. Prioridade média, com janela de execução em ambiente controlado."
}

```

**Tratamento de Erros**

* **Contexto insuficiente:** Se não for possível identificar módulos afetados, retornar lista vazia e alertar que a análise foi limitada
* **Projeto não mapeado:** Se `project_context.structure` não estiver disponível, fazer a análise apenas com base na issue
* **Estimativa incerta:** Se a pontuação de complexidade estiver em uma zona limítrofe, retornar uma faixa (ex: "medio_grande")

**Boas Práticas**

* **Sempre cite as fontes:** Indique de onde veio a informação (título, body, comentário, contexto)
* **Seja específico:** Use nomes reais de módulos, arquivos e funções
* **Considere o projeto:** Leve em conta a stack, arquitetura e convenções do projeto
* **Indique incertezas:** Use "provavelmente", "possivelmente" quando não tiver certeza
* **Foque em ação:** Todo risco deve ter uma mitigação sugerida