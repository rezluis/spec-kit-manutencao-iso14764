---
description: "Revisa a correção feita pelo Implementer antes de gerar testes"
---

## Objetivo

Revisar criticamente as mudanças de código feitas pelo `Implementer`, verificando conformidade com a `constitution.md`, cobertura do requisito da issue, qualidade do código e ausência de problemas óbvios. Emitir um **parecer (aprovado/rejeitado)** com justificativa detalhada.

## Entrada Esperada

```json
{
  "issue": {
    "number": 42,
    "title": "string",
    "body": "string"
  },
  "impact_report": {
    "classification": {"type": "corretiva"},
    "affected_modules": [...],
    "recommendations": {...}
  },
  "changes_made": {
    "files_created": [{"path": "...", "summary": "..."}],
    "files_modified": [{"path": "...", "summary": "..."}]
  },
  "diff": "string - diff unificado das mudanças"
}

```

## Processo de Revisão

### Etapa 1: Verificar Conformidade com a Issue

1. **Cobertura do requisito:** A mudança resolve o que a issue descreve?
2. **Escopo:** A mudança está limitada ao escopo da issue ou foi além?
3. **Efeitos colaterais:** Há mudanças em áreas não relacionadas à issue?

Se a mudança **não resolve o problema** ou **vai muito além do escopo**, rejeitar com justificativa.

### Etapa 2: Verificar Conformidade com a `constitution.md`

Ler a `.specify/memory/constitution.md` e verificar cada ponto:

| Item | Verificação |
| :--- | :--- |
| **Linguagem/versão** | O código usa a linguagem e versão corretas? |
| **Framework** | Usa o framework/bibliotecas obrigatórias? |
| **Arquitetura** | Respeita as camadas (controller $\rightarrow$ service $\rightarrow$ repository)? |
| **Padrões de código** | Nomenclatura, estilo, formatação? |
| **Segurança** | Não introduz vulnerabilidades? Não expõe secrets? |
| **Testes** | Segue o padrão de testes do projeto? |

### Etapa 3: Análise de Qualidade do Código

Aplicar checklist de boas práticas:

* [ ] O código é legível e autoexplicativo?
* [ ] Há tratamento de erros apropriado?
* [ ] Há comentários apenas onde necessário?
* [ ] Há duplicação de código?
* [ ] Há código morto ou imports não utilizados?
* [ ] A lógica está correta?
* [ ] Casos de borda foram considerados?

### Etapa 4: Análise de Regressão

Verificar se a mudança pode quebrar funcionalidades existentes:

1. **Interfaces públicas:** Endpoints, funções exportadas, tipos públicos?
2. **Dependências:** Bibliotecas que dependem do código alterado?
3. **Contratos:** API contracts, schemas, tipos?
4. **Configurações:** Variáveis de ambiente, configs?

### Etapa 5: Emitir Parecer

Gerar um parecer estruturado:

```json
{
  "verdict": "approved|rejected",
  "confidence": "alta|media|baixa",
  "issues_found": [
    {
      "severity": "critical|major|minor",
      "file": "string",
      "line": 42,
      "description": "string",
      "suggestion": "string"
    }
  ],
  "positives": [
    "Pontos positivos da mudança"
  ],
  "constitution_compliance": {
    "compliant": true,
    "violations": []
  },
  "summary": "Texto explicando o parecer"
}
```
**Critérios de rejeição automática:**[cite: 23]

* Viola a `constitution.md` em pontos críticos (segurança, arquitetura)[cite: 23]
* Não resolve o problema da issue[cite: 23]
* Introduz vulnerabilidade de segurança[cite: 23]
* Quebra interfaces públicas sem justificativa[cite: 23]

### Saída

```json
{
  "status": "approved|rejected",
  "report_path": ".specify/maintenance/reviews/issue-{number}-review.md",
  "verdict": {...},
  "next_action": "generate_tests|return_to_implementer"
}
```
**Exemplo de Uso**[cite: 24]

**Entrada:** Diff com mudança no `AuthController` que retorna 401.[cite: 24]

**Saída:**[cite: 24]

```json
{
  "status": "approved",
  "verdict": {
    "verdict": "approved",
    "confidence": "alta",
    "issues_found": [
      {
        "severity": "minor",
        "file": "src/controllers/auth.controller.ts",
        "line": 48,
        "description": "Comentário desatualizado na linha 48",
        "suggestion": "Atualizar comentário para refletir novo comportamento"
      }
    ],
    "positives": [
      "Corretamente retorna 401 em vez de propagar exceção",
      "Preserva comportamento para credenciais válidas",
      "Segue o padrão dos demais controllers"
    ],
    "constitution_compliance": {"compliant": true, "violations": []}
  },
  "next_action": "generate_tests"
}
```
### Tratamento de Erros[cite: 20]

| Erro | Ação |
| :--- | :--- |
| Diff vazio | Rejeitar: "Nenhuma mudança foi feita"[cite: 20] |
| Arquivo ausente no diff | Rejeitar: "Arquivo X foi mencionado mas não está no diff"[cite: 20] |
| `constitution.md` não encontrada | Avisar e prosseguir com boas práticas genéricas[cite: 20] |

### Boas Práticas[cite: 20]

* **Seja rigoroso:** O objetivo é pegar problemas antes dos testes[cite: 20]
* **Seja específico:** Aponte arquivo, linha e sugestão de correção[cite: 20]
* **Distinga severidade:** `critical` bloqueia, `major` requer correção, `minor` é sugestão[cite: 20]
* **Documente o positivo:** Reconhecer boas práticas incentiva consistência[cite: 20]
* **Não reescreva o código:** Apenas aponte o que precisa ser corrigido[cite: 20]


