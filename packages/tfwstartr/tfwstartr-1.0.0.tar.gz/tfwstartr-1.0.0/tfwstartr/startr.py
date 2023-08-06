import yaml
import os
import shutil
import secrets
import tempfile
import requests
import importlib.resources
from functools import cached_property
from typing import Dict, Optional, Union
from pathlib import Path
from tfwstartr.config import STARTER_WORKDIR, DATA_FOLDER
from tfwstartr.utils import GitHelper, PackageManager


class Startr:
    def __init__(self) -> None:
        self._git_helper = GitHelper()
        self._archive: Union[str, Path] = ""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if os.path.exists(self._archive):
            os.remove(self._archive)

    @staticmethod
    def get_starters():
        data = importlib.resources.read_text(DATA_FOLDER, "languages.yaml")
        return yaml.safe_load(data)

    @staticmethod
    def get_supported_packages(package_manager: str) -> Dict[str, str]:
        return PackageManager.get_supported_packages(package_manager)

    @classmethod
    def get_starter_requirements(
        cls, language_name: str, framework_name: str, starter_name: str
    ) -> Dict[str, str]:
        starters = cls.get_starters()
        repo_url: str = starters.get(language_name).get("repo")
        branch: str = (
            starters.get(language_name)
            .get("frameworks")
            .get(framework_name)
            .get("starters")
            .get(starter_name)
            .get("branch")
        )
        dependency_file: str = (
            starters.get(language_name)
            .get("frameworks")
            .get(framework_name)
            .get("starters")
            .get(starter_name)
            .get("dependency_file")
        )
        package_manager: str = (
            starters.get(language_name)
            .get("frameworks")
            .get(framework_name)
            .get("starters")
            .get(starter_name)
            .get("package_manager")
        )
        return PackageManager.get_required_packages(
            file_content=cls.__get_file_content(repo_url, branch, dependency_file),
            package_manager=package_manager,
        )

    def generate_starter(
        self,
        language_name: str,
        framework_name: str,
        starter_name: str,
        extra_packages: Optional[Dict[str, str]] = None,
    ) -> Union[str, Path]:
        starters = self.get_starters()
        repo_url: str = starters.get(language_name).get("repo")
        branch: str = (
            starters.get(language_name)
            .get("frameworks")
            .get(framework_name)
            .get("starters")
            .get(starter_name)
            .get("branch")
        )
        package_manager: str = (
            starters.get(language_name)
            .get("frameworks")
            .get(framework_name)
            .get("starters")
            .get(starter_name)
            .get("package_manager")
        )
        dependency_file: str = (
            starters.get(language_name)
            .get("frameworks")
            .get(framework_name)
            .get("starters")
            .get(starter_name)
            .get("dependency_file")
        )

        with tempfile.TemporaryDirectory() as workdir:
            self._git_helper.clone_repo(repo_url, workdir, branch)
            if extra_packages:
                PackageManager.install_packages(
                    workdir=workdir,
                    packages=extra_packages,
                    dependency_file=dependency_file,
                    package_manager=package_manager,
                )

            self.__cleanup_directory(os.path.join(workdir, ".git"))
            self._git_helper.init_starter_repo(workdir)
            self._archive = self.__generate_zip(
                archive_name=os.path.join(
                    STARTER_WORKDIR, f"{starter_name}-{secrets.token_hex(6)}"
                ),
                directory=workdir,
            )
            return self._archive

    @staticmethod
    def __cleanup_directory(dir_path: Union[str, Path]) -> None:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def __generate_zip(
        archive_name: str, directory: Union[str, Path]
    ) -> Union[str, Path]:
        return shutil.make_archive(
            base_name=archive_name,
            format="zip",
            root_dir=directory,
        )

    @staticmethod
    def __get_file_content(repo: str, branch: str, dependency_file: str) -> str:
        url = f"{repo.replace('github.com', 'raw.githubusercontent.com')}/{branch}/{dependency_file}"
        return requests.get(url).text
