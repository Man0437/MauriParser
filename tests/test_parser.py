import pytest

from pathlib import Path
from mauri.parser.parser import Parser
from mauri.parser.terminalparse import TerminalParser
from mauri.utils.settings import HTML_DIR, COOKIES_DIR, CONFIG_DIR, LOG_DIR


def test_is_inside_project():
    base = Path(__file__).resolve().parents[1]
    config = base / "pyproject.toml"

    assert base in config.parents

def test_config():
    path = Path(__file__).resolve().parents[1]

    path_base = path / "src" / "mauri"

    html_path = path_base / "html"
    config_path = path_base / "config"
    log_path = path_base / "logs"
    cookies_path = path_base / "cookies"

    assert HTML_DIR == html_path
    assert CONFIG_DIR == config_path
    assert LOG_DIR == log_path
    assert COOKIES_DIR == cookies_path