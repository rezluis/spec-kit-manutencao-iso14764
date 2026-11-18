---
description: "Executa a implementação da manutenção com base no relatório de impacto"
---

# Comando: Implementação de Manutenção

Este comando aciona o fluxo de implementação para uma issue já analisada.

## Entrada do Usuário
$ARGUMENTS

## Instruções para o Agente

Você deve executar o seguinte fluxo de trabalho:

1. **Identificar a Issue:** Da entrada em `$ARGUMENTS`, extraia o `owner`, `repo` e `issue_number`.

2. **Localizar o Relatório de Impacto:** Leia o relatório gerado previamente em `.specify/maintenance/analysis/issue-{issue_number}-impact.md` (ou `.specify/maintenance/analysis/issue-{issue_number}.md`). Se o relatório não existir, notifique o usuário e sugira executar primeiro `/speckit.maintenance.analyze`.

3. **Acionar o Implementer Agent:** Invoke o agente `implementer` passando como entrada:
   - O relatório de impacto completo
   - O contexto do projeto (leia a `constitution.md` e as `rules/`)
   - O número da issue

4. **Implementar a Mudança:** O `Implementer` deve:
   - Ler a `constitution.md` do projeto
   - Criar a branch apropriada
   - Invocar a skill `code-generator` para gerar o código
   - Invocar a skill `doc-updater` para atualizar a documentação
   - Executar lint e testes
   - Criar commit e abrir Pull Request (se configurado)

5. **Gerar Relatório de Implementação:** Salve o resultado em `.specify/maintenance/implementation/issue-{issue_number}-implementation.md`.

6. **Finalizar:** Informe ao usuário:
   - O link do Pull Request aberto
   - Os arquivos modificados
   - O status dos testes
   - Próximos passos (revisão, merge)
