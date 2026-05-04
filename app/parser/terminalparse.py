import requests
import argparse

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class SilentArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError("Error")

class TerminalParser:
    def __init__(self):
        self.parser = SilentArgumentParser()

        self.pipe = self.parser.add_subparsers(dest="entity", required=True)

        # Books
        books = self.pipe.add_parser("books")
        books_sub = books.add_subparsers(dest="action", required=True)

        books_list = books_sub.add_parser("list")
        books_list.add_argument("-i", required=False)
        books_list.add_argument("-n", required=False)
        books_list.add_argument("-t", required=False)
        books_list.add_argument("-a", required=False)
        books_list.add_argument("-p", required=False)
        books_list.add_argument("-m", required=False)

        books_delete = books_sub.add_parser("delete")
        books_delete.add_argument("-a", required=False)

        # UI - Для вывод окна и работы с UI приложения

        ui_pars = self.pipe.add_parser("ui")

        # Потом нужно протестировать

        # Добавление парсера для парса страниц из браузера
        parse_browser = self.pipe.add_parser("parse")


    def print_help(self):
        
        print("""Commands:
- list -
- add -
- delete -""")