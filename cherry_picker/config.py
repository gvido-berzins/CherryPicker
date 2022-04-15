from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any, Callable, List, Optional, Type, TypeVar, cast

import yaml

from cherry_picker.exceptions import InvalidConfigException
from context import CONFIG_PATH

T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Database:
    patterns: Optional[List[str]] = None
    paths: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Database":
        assert isinstance(obj, dict)
        patterns = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("patterns")
        )
        paths = from_union([lambda x: from_list(Path, x), from_none], obj.get("paths"))
        return Database(patterns, paths)

    def to_dict(self) -> dict:
        result: dict = {}
        result["patterns"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.patterns
        )
        result["paths"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.paths
        )
        return result


@dataclass
class Server:
    host: Optional[str] = None
    port: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Server":
        assert isinstance(obj, dict)
        host = from_union([from_str, from_none], obj.get("host"))
        port = from_union([from_int, from_none], obj.get("port"))
        return Server(host, port)

    def to_dict(self) -> dict:
        result: dict = {}
        result["host"] = from_union([from_str, from_none], self.host)
        result["port"] = from_union([from_int, from_none], self.port)
        return result


@dataclass
class CherryConfig:
    database: Optional[Database] = None
    server: Optional[Server] = None

    @staticmethod
    def from_dict(obj: Any) -> "CherryConfig":
        if not isinstance(obj, dict):
            raise InvalidConfigException()
        database = from_union([Database.from_dict, from_none], obj.get("database"))
        server = from_union([Server.from_dict, from_none], obj.get("server"))
        return CherryConfig(database, server)

    def to_dict(self) -> dict:
        result: dict = {}
        result["database"] = from_union(
            [lambda x: to_class(Database, x), from_none], self.database
        )
        result["server"] = from_union(
            [lambda x: to_class(Server, x), from_none], self.server
        )
        return result


def cherry_config_from_dict(s: Any) -> CherryConfig:
    return CherryConfig.from_dict(s)


def cherry_config(path: Path = CONFIG_PATH):
    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config = load_config(path)
            return func(config, *args, **kwargs)

        return wrapper

    return outer


def load_config(config_path: Path = CONFIG_PATH):
    data = yaml.safe_load(config_path.read_bytes())
    return cherry_config_from_dict(data)
