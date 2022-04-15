from pathlib import Path
from typing import Any

import pytest

from cherry_picker.config import (
    CherryConfig,
    Database,
    Server,
    cherry_config,
    load_config,
)
from cherry_picker.exceptions import InvalidConfigException
from tests import DATA_DIR


@pytest.fixture(scope="module")
def default_config() -> CherryConfig:
    """Expected default configuration fixture"""
    return CherryConfig(
        database=Database(patterns=["*.ctb", "*.db"], paths=[Path("/some/path")]),
        server=Server(host="0.0.0.0", port=5000),
    )


def test_load_config_full(default_config: CherryConfig):
    """Test fully filled configuration loading"""
    config = load_config(DATA_DIR / "default_config.yaml")
    assert config == default_config


def test_load_config_partial():
    """Test whether partially filled config is loaded appropriatly"""
    config = load_config(DATA_DIR / "partial_config.yaml")
    assert config == CherryConfig(
        database=Database(patterns=["*.ctb"]), server=Server(port=5000)
    )


def test_load_config_empty():
    """Test whether the config loader raises an error on an invalid config"""
    with pytest.raises(InvalidConfigException):
        load_config(DATA_DIR / "empty_config.yaml")


def test_cherry_config(default_config: CherryConfig):
    """Test whether the config decorator works as expected"""

    @cherry_config(path=DATA_DIR / "default_config.yaml")
    def func(cfg: CherryConfig, arg: int):
        return cfg, arg + 10

    assert func(1) == (default_config, 11)
