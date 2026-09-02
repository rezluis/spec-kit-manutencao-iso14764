"""
Base classes and interfaces for integrations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Issue:
    """Representação de uma Issue (Jira, GitHub, etc.)."""
    id: str
    title: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    labels: List[str] = None
    assignee: Optional[str] = None
    url: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class PullRequest:
    """Representação de um Pull Request (GitHub) ou Merge Request (GitLab)."""
    number: int
    title: str
    description: str
    state: str  # open, closed, merged
    created_at: datetime
    updated_at: datetime
    source_branch: str
    target_branch: str
    author: str
    reviewers: List[str] = None
    labels: List[str] = None
    url: str = None
    metadata: Dict[str, Any] = None


@dataclass
class Repository:
    """Representação de um repositório Git."""
    name: str
    owner: str
    description: str
    default_branch: str
    clone_url: str
    web_url: str
    is_private: bool = False
    metadata: Dict[str, Any] = None


@dataclass
class LogEntry:
    """Representação de uma entrada de log."""
    timestamp: datetime
    level: str  # ERROR, WARN, INFO, DEBUG
    message: str
    source: str  # ex: "TaskController", "TaskService"
    stack_trace: Optional[str] = None
    metadata: Dict[str, Any] = None


class IssueTracker(ABC):
    """Interface para sistemas de tracking de issues (Jira, GitHub Issues, etc.)."""

    @abstractmethod
    def get_issue(self, issue_id: str) -> Issue:
        """Obtém uma issue pelo ID."""
        pass

    @abstractmethod
    def create_issue(self, title: str, description: str, labels: List[str] = None) -> Issue:
        """Cria uma nova issue."""
        pass

    @abstractmethod
    def update_issue(self, issue_id: str, **kwargs) -> Issue:
        """Atualiza uma issue existente."""
        pass

    @abstractmethod
    def search_issues(self, query: str) -> List[Issue]:
        """Busca issues por query."""
        pass


class GitRepository(ABC):
    """Interface para operações em repositórios Git."""

    @abstractmethod
    def clone(self, repo_url: str, target_path: str) -> str:
        """Clona um repositório."""
        pass

    @abstractmethod
    def create_branch(self, repo_path: str, branch_name: str, base_branch: str = "main") -> bool:
        """Cria uma branch no repositório."""
        pass

    @abstractmethod
    def commit(self, repo_path: str, message: str, files: List[str] = None) -> str:
        """Faz commit de mudanças."""
        pass

    @abstractmethod
    def push(self, repo_path: str, branch_name: str) -> bool:
        """Envia mudanças para o repositório remoto."""
        pass

    @abstractmethod
    def create_pull_request(self, repo_path: str, source_branch: str, target_branch: str,
                           title: str, description: str, reviewers: List[str] = None) -> PullRequest:
        """Cria um Pull Request."""
        pass

    @abstractmethod
    def get_repository_info(self, repo_url: str) -> Repository:
        """Obtém informações do repositório."""
        pass


class Notifier(ABC):
    """Interface para sistemas de notificação (Slack, Email, etc.)."""

    @abstractmethod
    def send_notification(self, message: str, recipients: List[str], **kwargs) -> bool:
        """Envia uma notificação."""
        pass


class LogParser(ABC):
    """Interface para parsing de logs."""

    @abstractmethod
    def parse_line(self, line: str) -> Optional[LogEntry]:
        """Parseia uma linha de log."""
        pass

    @abstractmethod
    def parse_file(self, file_path: str) -> List[LogEntry]:
        """Parseia um arquivo de log completo."""
        pass