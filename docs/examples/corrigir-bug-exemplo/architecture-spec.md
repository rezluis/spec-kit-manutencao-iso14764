# Especificação da Arquitetura - Task Manager API

> **Nota:** Este documento foi gerado automaticamente pelo Architecture Understanding Agent a partir do código-fonte do repositório `https://github.com/example/task-manager-api` na data `2025-06-01`.

## 1. Visão Geral
- **Nome do Sistema:** Task Manager API
- **Tecnologias:** Java 17, Spring Boot 3.2.0, Maven, PostgreSQL 15
- **Padrão Arquitetural:** MVC com camada Service
- **Versão:** v2.1.0

## 2. Estrutura de Pacotes
| Pacote | Camada | Responsabilidade |
|--------|--------|------------------|
| `com.taskmanager.controller` | Controller | Endpoints REST, validação |
| `com.taskmanager.service` | Service | Lógica de negócio, transações |
| `com.taskmanager.repository` | Repository | Acesso a dados JPA |
| `com.taskmanager.dto` | DTO | Transferência de dados |
| `com.taskmanager.entity` | Entity | Mapeamento JPA |
| `com.taskmanager.config` | Config | Configurações Spring |

## 3. Endpoints Relevantes
| Método | Path | Controller | Método Java |
|--------|------|------------|-------------|
| PUT | `/api/tasks/{id}` | TaskController | `updateTask(Long id, TaskUpdateDTO dto)` |

## 4. Entidade `Task` (resumido)
- `id`: Long (PK)
- `title`: String (not null)
- `description`: String
- `status`: StatusEnum (TODO, IN_PROGRESS, DONE)
- `dueDate`: LocalDate (pode ser nulo)
- `user`: User (ManyToOne)

## 5. Regras de Negócio Identificadas
- Título não pode ser vazio.
- Status só pode ser alterado se a tarefa existir.
- A data de vencimento (dueDate) pode ser nula, mas se presente deve ser futura.

## 6. Dependências Externas
- PostgreSQL (produção)
- H2 (testes)