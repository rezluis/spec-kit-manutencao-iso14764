"""
Cliente GitHub - Wrapper para PyGithub.
"""

import os
from typing import Optional, Dict, Any
from github import Github, GithubException
from github import Auth
from ..base import Repository, Issue, PullRequest


class GitHubClient:
    """Cliente para API do GitHub."""

    def __init__(self, token: Optional[str] = None, base_url: str = "https://api.github.com"):
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token not provided. Set GITHUB_TOKEN env var.")
        
        self.base_url = base_url
        self.client = Github(self.token, base_url=self.base_url)
    
    def get_repo(self, owner: str, repo_name: str) -> Repository:
        """Obtém informações de um repositório."""
        try:
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            return Repository(
                name=repo.name,
                owner=repo.owner.login,
                description=repo.description or "",
                default_branch=repo.default_branch,
                clone_url=repo.clone_url,
                web_url=repo.html_url,
                is_private=repo.private,
                metadata={
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "open_issues": repo.open_issues_count
                }
            )
        except GithubException as e:
            raise Exception(f"GitHub API error: {e.data.get('message', str(e))}")

    def create_issue(self, owner: str, repo_name: str, title: str, body: str, 
                     labels: list = None) -> Issue:
        """Cria uma issue no GitHub."""
        try:
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            issue = repo.create_issue(title=title, body=body, labels=labels or [])
            
            return Issue(
                id=str(issue.number),
                title=issue.title,
                description=issue.body or "",
                status=issue.state,
                priority="N/A",  # GitHub não tem prioridade nativa
                created_at=issue.created_at,
                updated_at=issue.updated_at,
                labels=[l.name for l in issue.labels],
                assignee=issue.assignee.login if issue.assignee else None,
                url=issue.html_url
            )
        except GithubException as e:
            raise Exception(f"GitHub API error: {e.data.get('message', str(e))}")

    def create_pull_request(self, owner: str, repo_name: str, title: str, body: str,
                           head_branch: str, base_branch: str,
                           labels: list = None, reviewers: list = None) -> PullRequest:
        """Cria um Pull Request no GitHub."""
        try:
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )
            
            if labels:
                pr.add_to_labels(*labels)
            
            if reviewers:
                pr.create_review_request(reviewers=reviewers)
            
            return PullRequest(
                number=pr.number,
                title=pr.title,
                description=pr.body or "",
                state=pr.state,
                created_at=pr.created_at,
                updated_at=pr.updated_at,
                source_branch=head_branch,
                target_branch=base_branch,
                author=pr.user.login,
                reviewers=reviewers or [],
                labels=labels or [],
                url=pr.html_url
            )
        except GithubException as e:
            raise Exception(f"GitHub API error: {e.data.get('message', str(e))}")