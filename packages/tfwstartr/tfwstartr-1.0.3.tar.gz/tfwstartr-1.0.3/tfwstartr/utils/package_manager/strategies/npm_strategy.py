import os
import json
from typing import Dict, Union
from pathlib import Path
from .strategy_base import PackageManagerStrategy


class NpmStrategy(PackageManagerStrategy):
    @staticmethod
    def install_packages(
        workdir: Union[str, Path], dependency_file: str, packages: Dict[str, str]
    ) -> None:
        with open(os.path.join(workdir, dependency_file), "r") as requirements:
            packagejson = json.loads(requirements.read())
        for name, version in packages.items():
            packagejson["dependencies"][name] = version
        with open(os.path.join(workdir, dependency_file), "w+") as requirements:
            requirements.write(json.dumps(packagejson, indent=2))

    @staticmethod
    def get_packages_from_file(file_content: str) -> Dict[str, str]:
        return json.loads(file_content).get("dependencies")
