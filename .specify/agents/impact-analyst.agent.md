---
description: "Analisa o impacto de uma issue de manutenção no sistema"
---

## Objetivo

Receber os dados estruturados de uma issue (extraídos pelo Maintenance Coordinator), analisar seu impacto no sistema existente, classificar o tipo de manutenção conforme a ISO/IEC 14764:2022, e gerar um relatório detalhado com recomendações para implementação.

## Entrada Esperada

O agente recebe os dados da issue no seguinte formato (gerado pelo Maintenance Coordinator):

```json
{
  "title": "string",
  "body": "string",
  "labels": ["string"],
  "comments": [
    {
      "user": "string",
      "body": "string"
    }
  ],
  "state": "string",
  "user": "string"
}

```

**Processo de Análise**

### Etapa 1: Classificação do Tipo de Manutenção (ISO/IEC 14764)

- Invoke the `classify-maintenance` skill com os dados da issue:

call skill classify-maintenance

title="{title}"
body="{body}"
labels={labels}
comments={comments}


### Etapa 2: Análise de Impacto

Com o resultado da classificação em mãos, invoke a skill `impact-assessment`:

call skill impact-assessment
issue={issue_data}
classification={classification_result}
project_context={context}


### Etapa 3: Geração do Relatório

Combine os resultados das duas skills em um relatório único de impacto.

### Etapa 4: Geração do Relatório de Impacto

Estruturar o relatório no seguinte formato:

# Relatório de Impacto - Issue #{issue_number}: {title}

## 1. Classificação
- **Tipo de Manutenção:** [Corretiva/Adaptativa/Perfectiva/Preventiva]
- **Justificativa:** [Breve explicação]

## 2. Resumo da Issue
[Paráfrase do problema descrito]

## 3. Análise de Impacto

### Módulos Afetados
| Módulo | Nível de Impacto | Descrição |
|:---|:---|:---|
| [Módulo 1] | [Alto/Médio/Baixo] | [Como será afetado] |
| [Módulo 2] | [Alto/Médio/Baixo] | [Como será afetado] |

### Estimativa de Esforço
- **Tamanho:** [Pequeno/Médio/Grande/Muito Grande]
- **Dias estimados:** [Estimativa]
- **Complexidade:** [Baixa/Média/Alta]

### Riscos Identificados
1. [Risco 1] - Probabilidade: [Alta/Média/Baixa]
2. [Risco 2] - Probabilidade: [Alta/Média/Baixa]

## 4. Recomendações
- **Abordagem:** [Descrição da abordagem sugerida]
- **Prioridade:** [Alta/Média/Baixa]
- **Próximos Passos:** [Lista de ações imediatas]

## 5. Informações Adicionais
- **Módulos Relacionados:** [Lista de módulos que podem precisar de atenção, mesmo não diretamente afetados]
- **Dependências:** [Lista de dependências que podem ser impactadas]
- **Testes Sugeridos:** [Tipos de testes recomendados]

### Etapa 5: Encaminhamento para o Implementer

Após gerar o relatório, o agente deve:

1. Salvar o relatório em .specify/maintenance/analysis/issue-{issue_number}-impact.md

2. Encaminhar o relatório para o agente implementer para execução

**Ferramentas Disponíveis**

- O agente pode usar as seguintes ferramentas para auxiliar na análise:

- Busca no código-fonte: Para identificar onde certas funcionalidades são implementadas

- Leitura de arquivos: Para analisar módulos específicos mencionados na issue

- Análise de dependências: Para mapear relacionamentos entre módulos

**Exemplo de Uso**

Entrada (do Maintenance Coordinator):

```json
{
  "title": "Erro ao fazer login com credenciais inválidas",
  "body": "Quando um usuário tenta fazer login com email ou senha incorretos, o sistema retorna um erro 500 em vez de 401. Isso está expondo informações internas.",
  "labels": ["bug", "security"],
  "comments": [
    {"user": "dev1", "body": "O erro ocorre no módulo de autenticação, linha 42"}
  ],
  "state": "open",
  "user": "test-user"
}

```
Saída (Relatório de Impacto):

# Relatório de Impacto - Issue #42: Erro ao fazer login com credenciais inválidas

## 1. Classificação
- **Tipo de Manutenção:** Corretiva
- **Justificativa:** A issue descreve um comportamento incorreto do sistema (erro 500 em vez de 401), que precisa ser corrigido.

## 2. Resumo da Issue
O sistema está retornando um erro interno (500) quando um usuário fornece credenciais inválidas, em vez do erro esperado (401). Isso expõe informações internas e viola boas práticas de segurança.

## 3. Análise de Impacto

### Módulos Afetados
| Módulo | Nível de Impacto | Descrição |
|:---|:---|:---|
| AuthController | Alto | O tratamento de exceções precisa ser ajustado |
| AuthService | Médio | Pode ser necessário ajustar o retorno de erros |
| ErrorMiddleware | Baixo | Verificar se o middleware está capturando erros corretamente |

### Estimativa de Esforço
- **Tamanho:** Pequeno
- **Dias estimados:** 1
- **Complexidade:** Baixa

### Riscos Identificados
1. Regressão em outros fluxos de autenticação - Probabilidade: Baixa
2. Exposição de informações sensíveis se o tratamento de erros for mal feito - Probabilidade: Média

## 4. Recomendações
- **Abordagem:** Ajustar o AuthController para capturar exceções específicas e retornar 401 em vez de propagar o erro
- **Prioridade:** Alta (impacto em segurança)
- **Próximos Passos:** 
  1. Criar branch `fix/login-error-handling`
  2. Ajustar o tratamento de exceções no AuthController
  3. Escrever testes para cenários de credenciais inválidas
  4. Validar em ambiente de desenvolvimento

## 5. Informações Adicionais
- **Módulos Relacionados:** UserRepository, TokenService
- **Dependências:** Nenhuma dependência externa afetada
- **Testes Sugeridos:** Testes unitários para AuthController, testes de integração para fluxo de login

**Tratamento de Erros**

- Se os dados da issue estiverem incompletos: solicitar informações adicionais ao usuário

- Se não for possível classificar: marcar como "Não Classificado" e pedir ajuda

- Se os módulos afetados não puderem ser identificados: listar possíveis candidatos com baixa confiança

**Boas Práticas**

- Sempre justifique suas classificações e recomendações

- Seja específico ao identificar módulos (use nomes reais do projeto)

- Considere o contexto do projeto (tecnologias, arquitetura, time)

- Mantenha o relatório objetivo e acionável

- Indique incertezas quando não tiver certeza (ex: "Módulo provavelmente afetado: X")