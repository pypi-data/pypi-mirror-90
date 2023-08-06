import yaml
import importlib.resources
from typing import Dict, Union
from pathlib import Path
from tfwstartr.config import DATA_FOLDER
from .strategies import strategy_mapping


class PackageManager:
    @staticmethod
    def install_packages(
        workdir: Union[str, Path],
        dependency_file: str,
        packages: Dict[str, str],
        package_manager: str,
    ) -> None:
        strategy = strategy_mapping.get(package_manager)
        strategy.install_packages(
            workdir=workdir, dependency_file=dependency_file, packages=packages
        )

    @staticmethod
    def get_required_packages(
        file_content: str, package_manager: str
    ) -> Dict[str, str]:
        strategy = strategy_mapping.get(package_manager)
        return strategy.get_packages_from_file(file_content)

    @staticmethod
    def get_supported_packages(package_manager: str) -> Dict[str, str]:
        try:
            data = importlib.resources.read_text(DATA_FOLDER, f"{package_manager}.yaml")
        except:
            return {}
        return yaml.safe_load(data).get("packages")
