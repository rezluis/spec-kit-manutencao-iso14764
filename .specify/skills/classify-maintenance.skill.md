---
description: "Classifica uma issue de manutenção conforme a ISO/IEC 14764:2022"
---

## Propósito
Esta skill analisa o texto de uma issue (título, descrição, labels, comentários) e a classifica em um dos 4 tipos de manutenção definidos pela ISO/IEC 14764:2022, fornecendo uma justificativa clara para a classificação.

## Entrada
- `title` (string): Título da issue
- `body` (string): Descrição completa da issue
- `labels` (array de strings): Labels associadas à issue
- `comments` (array de objetos): Comentários da issue (cada um com `user` e `body`)

## Processo de Classificação

### Passo 1: Coletar e Normalizar o Texto
1. Concatenar `title`, `body`, `labels` e o texto dos `comments`
2. Converter tudo para minúsculas para facilitar a análise
3. Remover caracteres especiais e pontuação desnecessária

### Passo 2: Aplicar Regras de Classificação

#### Critérios para Manutenção Corretiva
**Indicadores fortes:**
- Palavras-chave: `bug`, `error`, `falha`, `crash`, `exception`, `incorreto`, `quebrou`, `parou`, `não funciona`, `problema`, `defeito`, `issue`, `fix`, `corrigir`, `arrumar`, `erro`, `stack trace`, `null pointer`, `undefined`, `memory leak`
- Labels: `bug`, `fix`, `hotfix`, `error`, `critical`, `regression`
- Contexto: Descrição de um comportamento que deveria funcionar mas não funciona

**Exemplo:** "Quando clico em salvar, o sistema trava com erro 500"

#### Critérios para Manutenção Adaptativa
**Indicadores fortes:**
- Palavras-chave: `atualização`, `upgrade`, `versão`, `version`, `compatibilidade`, `compatibility`, `dependência`, `dependency`, `migração`, `migration`, `nova versão`, `new version`, `ambiente`, `environment`, `os`, `sistema operacional`, `framework`, `api`, `endpoint mudou`
- Labels: `dependencies`, `upgrade`, `migration`, `compatibility`, `environment`
- Contexto: Mudança no ambiente externo que exige adaptação do software

**Exemplo:** "Atualizar a biblioteca X para a versão 3.0 devido a fim de suporte"

#### Critérios para Manutenção Perfectiva
**Indicadores fortes:**
- Palavras-chave: `melhoria`, `improvement`, `otimização`, `optimization`, `performance`, `usabilidade`, `usability`, `refatoração`, `refactor`, `qualidade`, `quality`, `experiência`, `experience`, `ux`, `mais rápido`, `faster`, `legibilidade`, `readability`, `manutenibilidade`, `maintainability`, `debt`, `dívida técnica`
- Labels: `enhancement`, `improvement`, `performance`, `refactor`, `ux`, `quality`, `tech-debt`
- Contexto: Melhoria de algo que já funciona, mas pode ser melhorado

**Exemplo:** "Melhorar o tempo de resposta da API de busca para menos de 200ms"

#### Critérios para Manutenção Preventiva
**Indicadores fortes:**
- Palavras-chave: `prevenção`, `prevention`, `segurança`, `security`, `vulnerabilidade`, `vulnerability`, `risco`, `risk`, `futuro`, `future`, `potencial`, `potential`, `cve`, `patch`, `backup`, `disaster recovery`, `failover`, `auditoria`, `audit`
- Labels: `security`, `vulnerability`, `risk`, `preventive`, `audit`, `compliance`
- Contexto: Ações para evitar problemas futuros, antes que eles ocorram

**Exemplo:** "Atualizar biblioteca de criptografia para corrigir vulnerabilidade CVE-2024-XXXX"

### Passo 3: Regras de Desempate e Priorização

Se múltiplos tipos forem identificados, aplicar a seguinte ordem de prioridade:

**Prioridade 1 - Corretiva:** Se há evidência de um defeito ou comportamento incorreto que afeta a funcionalidade atual, classificar como Corretiva.
**Justificativa:** Correção de defeitos é a prioridade mais alta, pois afeta diretamente os usuários.

**Prioridade 2 - Adaptativa:** Se há evidência de mudança no ambiente externo que exige adaptação.
**Justificativa:** Mantém o software funcionando em seu ambiente.

**Prioridade 3 - Perfectiva:** Se há evidência de melhoria sem caráter urgente.
**Justificativa:** Melhorias proativas são importantes mas podem ser agendadas.

**Prioridade 4 - Preventiva:** Se há evidência de ação preventiva.
**Justificativa:** Prevenção é importante mas geralmente menos urgente.

**Regra especial:** Se houver indicação de segurança (vulnerabilidade), a prioridade pode ser elevada para Corretiva ou Adaptativa, dependendo do contexto.

### Passo 4: Geração da Justificativa

Para cada classificação, gerar uma justificativa que inclua:

1. Quais palavras-chave ou padrões foram encontrados
2. Por que esses indicadores apontam para o tipo escolhido
3. Se houver ambiguidade, mencionar os tipos alternativos considerados

## Saída

A skill deve retornar um objeto JSON com a seguinte estrutura:

```json
{
  "classification": {
    "type": "corretiva|adaptativa|perfectiva|preventiva",
    "type_en": "corrective|adaptive|perfective|preventive",
    "confidence": "alta|media|baixa"
  },
  "keywords_found": ["palavra1", "palavra2"],
  "alternatives_considered": ["adaptativa", "preventiva"],
  "justification": "Texto explicando a classificação em português",
  "urgency": "alta|media|baixa"
}

```

## Explicação dos Campos

| Campo                 | Descrição                                                      |
|-----------------------|----------------------------------------------------------------|
| `type`                | Tipo de manutenção em português                               |
| `type_en`             | Tipo de manutenção em inglês (para referência)                |
| `confidence`          | Nível de confiança na classificação (alta, média, baixa)      |
| `keywords_found`      | Lista de palavras-chave que levaram à classificação            |
| `alternatives_considered` | Outros tipos que foram considerados mas descartados        |
| `justification`       | Justificativa completa da classificação                        |
| `urgency`              | Nível de urgência baseado na classificação e contexto         |

**Exemplo de Uso**

Exemplo 1: Manutenção Corretiva

Entrada:

```json

{
  "title": "Erro ao salvar usuário: campo email duplicado",
  "body": "Quando tento cadastrar um usuário com email já existente, o sistema retorna erro 500 em vez de uma mensagem amigável.",
  "labels": ["bug", "critical"],
  "comments": [
    {"user": "dev1", "body": "A exceção está sendo lançada no UserService linha 45"},
    {"user": "dev2", "body": "Isso afeta o fluxo de cadastro de novos clientes"}
  ]
}

```

Saida:

```json

{
  "classification": {
    "type": "corretiva",
    "type_en": "corrective",
    "confidence": "alta"
  },
  "keywords_found": ["erro", "retorna erro", "bug", "critical"],
  "alternatives_considered": [],
  "justification": "A issue descreve um comportamento incorreto do sistema (erro 500 em vez de mensagem amigável) que afeta o fluxo de cadastro. As labels 'bug' e 'critical' reforçam a classificação como corretiva. Não há evidências de adaptação a ambiente externo, melhoria ou prevenção.",
  "urgency": "alta"
}

```

**Exemplo 2: Manutenção Adaptativa**

Entrada:

```json

{
  "title": "Atualizar para Node.js 20 LTS",
  "body": "O Node.js 18 está em fim de vida. Precisamos atualizar para a versão 20 LTS para manter suporte e segurança.",
  "labels": ["dependencies", "upgrade"],
  "comments": [
    {"user": "dev1", "body": "É preciso verificar compatibilidade com as bibliotecas que usamos"},
    {"user": "dev2", "body": "Já testei localmente e parece funcionar"}
  ]
}

```

Saida:

```json

{
  "title": "Atualizar para Node.js 20 LTS",
  "body": "O Node.js 18 está em fim de vida. Precisamos atualizar para a versão 20 LTS para manter suporte e segurança.",
  "labels": ["dependencies", "upgrade"],
  "comments": [
    {"user": "dev1", "body": "É preciso verificar compatibilidade com as bibliotecas que usamos"},
    {"user": "dev2", "body": "Já testei localmente e parece funcionar"}
  ]
}

```

**Exemplo 3: Manutenção Perfectiva**

Entrada:

```json
{
  "title": "Otimizar consulta de relatórios mensais",
  "body": "O relatório mensal está demorando mais de 10 segundos para carregar. Precisamos otimizar a consulta SQL para melhorar a experiência do usuário.",
  "labels": ["performance", "enhancement"],
  "comments": [
    {"user": "dev1", "body": "A consulta atual faz vários joins desnecessários"},
    {"user": "dev2", "body": "Podemos adicionar índices e fazer cache dos resultados"}
  ]
}

```

Saída:

```json
{
  "classification": {
    "type": "perfectiva",
    "type_en": "perfective",
    "confidence": "alta"
  },
  "keywords_found": ["otimizar", "performance", "enhancement", "experiência"],
  "alternatives_considered": [],
  "justification": "A issue busca melhorar o desempenho de uma funcionalidade existente (relatórios mensais), sem correção de defeitos ou adaptação a ambiente externo. As labels 'performance' e 'enhancement' confirmam a classificação como perfectiva.",
  "urgency": "media"
}

```

**Exemplo 4: Manutenção Preventiva**

Entrada:

```json
{
  "title": "Atualizar biblioteca de criptografia para corrigir vulnerabilidade",
  "body": "A biblioteca CryptoJS versão 3.3 tem uma vulnerabilidade conhecida (CVE-2023-12345). Precisamos atualizar para a versão 4.0 ou superior.",
  "labels": ["security", "vulnerability"],
  "comments": [
    {"user": "dev1", "body": "A vulnerabilidade permite ataques de timing"},
    {"user": "sec-team", "body": "Prazo para correção: 30 dias"}
  ]
}

```

Saída:

```json
{
  "classification": {
    "type": "preventiva",
    "type_en": "preventive",
    "confidence": "alta"
  },
  "keywords_found": ["vulnerabilidade", "security", "vulnerability", "cve"],
  "alternatives_considered": ["adaptativa"],
  "justification": "A issue trata da correção de uma vulnerabilidade de segurança conhecida antes que ela seja explorada. Embora envolva atualização de biblioteca (que poderia ser adaptativa), o foco principal é a prevenção de um problema futuro, caracterizando manutenção preventiva.",
  "urgency": "alta"
}

```

## Tratamento de Erros

- Se não houver palavras-chave suficientes para uma classificação confiável, retornar `confidence: "baixa"` e marcar `type` como `"nao_classificado"`.
- Se a entrada estiver incompleta (sem título ou body), retornar erro de validação.

## Dicas para o Agente

- **Priorize labels:** Labels como `bug`, `security`, `enhancement` são indicadores fortes.
- **Analise o contexto:** Uma mesma palavra pode indicar tipos diferentes dependendo do contexto.
- **Considere o tom:** Descrições que mencionam "urgente", "crítico", "produção" sugerem maior prioridade.
- **Documente a dúvida:** Se não tiver certeza, inclua na justificativa quais informações adicionais seriam úteis.


