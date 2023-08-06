from typing import Dict, Type
from .strategy_base import PackageManagerStrategy
from .pip_strategy import PipStrategy
from .npm_strategy import NpmStrategy


strategy_mapping: Dict[str, Type[PackageManagerStrategy]] = {
    "pip": PipStrategy,
    "npm": NpmStrategy,
}
