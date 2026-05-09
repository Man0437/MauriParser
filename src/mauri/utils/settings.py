from pathlib import Path

DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = DIR / "config"
LOG_DIR = DIR / "logs"
HTML_DIR = DIR / "html"
COOKIES_DIR = DIR / "cookies" 

CONFIG_FILE = CONFIG_DIR / "parse.conf"
LOG_FILE = LOG_DIR / "mauri.logs"
HTML_FILE = HTML_DIR / "response.html"
COOKIES_FILE = COOKIES_DIR / "cookies.txt"