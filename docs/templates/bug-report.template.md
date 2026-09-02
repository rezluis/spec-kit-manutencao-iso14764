# Template de Relatório de Bug

## Instruções de Uso
Este template deve ser utilizado por desenvolvedores, clientes ou sistemas de monitoramento para reportar um bug que acionará o fluxo de manutenção corretiva.

---

# Relatório de Bug

## 1. Identificação
- **ID do Bug:** [GERADO AUTOMATICAMENTE PELO SISTEMA - ex: BUG-001]
- **Data do Reporte:** `YYYY-MM-DD HH:MM:SS`
- **Reportado por:** [Nome do usuário ou sistema]
- **Sistema/Componente:** [Ex: Módulo de Tarefas - API]

## 2. Título
[Forneça um título curto e descritivo, com até 10 palavras]

*Exemplo: "NullPointerException ao atualizar tarefa sem data de vencimento"*

## 3. Descrição do Problema
[Descreva o problema de forma clara e concisa]

*Exemplo: "Ao tentar atualizar uma tarefa que não possui data de vencimento (`due_date = null`), o sistema lança uma NullPointerException e não retorna uma mensagem de erro amigável ao usuário."*

## 4. Passos para Reproduzir
1. [Primeiro passo]
2. [Segundo passo]
3. [Terceiro passo]
...

*Exemplo:*
1. *Faça login como usuário válido*
2. *Crie uma tarefa com título e descrição, mas sem preencher a data de vencimento*
3. *Tente atualizar esta tarefa (PUT /tasks/{id}) com outro campo qualquer*

## 5. Comportamento Esperado
[Descreva o que deveria acontecer]

*Exemplo: "O sistema deveria retornar um erro 400 (Bad Request) com a mensagem 'A data de vencimento não pode ser nula'."*

## 6. Comportamento Atual
[Descreva o que realmente acontece]

*Exemplo: "O sistema lança uma NullPointerException e retorna um erro 500 (Internal Server Error) com stack trace no log."*

## 7. Ambiente
- **Sistema Operacional:** [Windows/Linux/macOS]
- **Navegador/Cliente:** [Chrome/Firefox/Postman/cURL]
- **Versão do Backend:** [Ex: v1.2.3 ou hash do commit]
- **Banco de Dados:** [PostgreSQL/MySQL/H2]

## 8. Evidências
### Logs / Stack Trace