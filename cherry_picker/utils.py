from pathlib import Path
from typing import Any


def find_databases(paths: list[Path], patterns: list[str]) -> list[Path]:
    """Find all SQLite databases in given paths and patterns"""
    dbs = []
    for path in paths:
        dbs.extend(search_path_for_databases(path, patterns))
    return dbs


def search_path_for_databases(path: Path, patterns: list[str]) -> list[Path]:
    """Search the given path for all datbases based on configured patterns"""
    return [file for pattern in patterns for file in path.glob(pattern)]


def pl(list_: list[Any]) -> None:
    [print(el) for el in list_]
