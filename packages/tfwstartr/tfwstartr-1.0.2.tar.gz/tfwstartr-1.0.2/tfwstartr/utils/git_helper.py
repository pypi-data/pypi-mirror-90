from typing import Optional, Union
from pathlib import Path
from git import Repo


class GitHelper:
    def __init__(self) -> None:
        self._default_init_message = "TFW starter initialized"

    @staticmethod
    def _add_and_commit(
        repo: Repo, message: str, author_name: str, author_email: str
    ) -> None:
        repo.git.add("--all")
        repo.git.commit("-m", message, author=f"{author_name} <{author_email}>")

    def init_starter_repo(
        self,
        repo_dir: Union[str, Path],
        user_name: str = "startR",
        user_email: str = "support@avatao.com",
        init_message: Optional[str] = None,
    ) -> None:
        repo = Repo.init(repo_dir, mkdir=False)
        with repo.config_writer() as config:
            config.set_value("user", "name", user_name)
            config.set_value("user", "email", user_email)
        self._add_and_commit(
            repo, init_message or self._default_init_message, user_name, user_email
        )

    @staticmethod
    def clone_repo(
        repo_url: str, repo_dir: Union[str, Path], branch: Optional[str] = None
    ) -> None:
        repo = Repo.clone_from(repo_url, repo_dir)
        if branch:
            repo.git.checkout(branch)
