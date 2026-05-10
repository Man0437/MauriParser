from pathlib import Path

DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = DIR / "config"
LOG_DIR = DIR / "logs"
HTML_DIR = DIR / "html"
COOKIES_DIR = DIR / "cookies"
FONT_DIR = DIR / "font"
ASSETS_DIR = DIR / "assets"

ICO_FILE = ASSETS_DIR / "mauri.ico"
PNG_FILE = ASSETS_DIR / "mauri.png"
FONT_ROBOTO_REGULAR = FONT_DIR / "Roboto.ttf"

CONFIG_FILE = CONFIG_DIR / "parse.conf"
LOG_FILE = LOG_DIR / "mauri.logs"
HTML_FILE = HTML_DIR / "response.html"
COOKIES_FILE = COOKIES_DIR / "cookies.txt"