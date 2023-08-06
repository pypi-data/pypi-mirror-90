import os
from typing import Dict, Union
from pathlib import Path
from .strategy_base import PackageManagerStrategy


class PipStrategy(PackageManagerStrategy):
    @staticmethod
    def install_packages(
        workdir: Union[str, Path], dependency_file: str, packages: Dict[str, str]
    ) -> None:
        with open(os.path.join(workdir, dependency_file), "a+") as requirements:
            if not requirements.read().endswith("\n"):
                requirements.write("\n")
            for name, version in packages.items():
                requirements.write(f"{name}=={version}\n")

    @staticmethod
    def get_packages_from_file(file_content: str) -> Dict[str, str]:
        packages = {}
        lines = file_content.split("\n")
        for line in lines:
            name, version = line.strip().split("==")
            packages[name] = version
        return packages
