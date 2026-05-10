from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from mauri.models.books import Books, BookRepository
from dataclasses import dataclass
from mauri.utils.settings import HTML_FILE, CONFIG_FILE, COOKIES_FILE
from mauri.utils.logger_ui import logger, log_queue

import requests
import os.path
import configparser
import logging
from mauri.utils.logger import setup_logger
import sys

setup_logger()
#logger = logging.getLogger(__name__)
# Если кому понадобится, то удобный вывод для записей с отпаршеного html, аналог Books.list() с другим выводом

def print_books(name, author, type, price_n, i):
    print(f"Название: {name}\nАвтор: {author}\nТип: {type}\nЦена: {price_n}\n___{i}___")


class Parser():
    def __init__(self):
        # cookies - поля для куки, поле класса
        # browser - Браузер для работы, поле класса ?? Пока не поле класса
        # context - поле класса
    
        # Можно добавить еще поле для самого парсера, но я не знаю зачем
        self.config = configparser.ConfigParser()
        
        try:
            self.config.read(CONFIG_FILE)
            self.update_html_bool: bool = self.config.getboolean("parsing", "UPDATE_HTML")
        except configparser.NoSectionError:
            logger.error("Ошибка при чтении конфига")
            sys.exit(0)
        logger.info("ОК | Прочитан конфиг")
        logger.info(f"Выставленное значение - {self.update_html_bool}")

        self.books = BookRepository()
        with sync_playwright() as p:
            self.browser = p.firefox.launch()
            self.context = self.browser.new_context()
            page = self.context.new_page()
            page.goto("https://www.books.ru/")
            page.wait_for_timeout(1000)
            cookies = self.context.cookies()
            self.browser.close()

        logger.info("OK | Браузер")
        self.cookie_dict = {c['name']: c['value'] for c in cookies}
        logger.info("OK | Cookie")

    def check_files(self):
        if(os.path.exists(COOKIES_FILE)):
            pass
        else:
            with open(COOKIES_FILE, mode="w") as file:
                import json
                file.write(json.dumps(self.cookie_dict))

        if(os.path.exists(HTML_FILE)):
            pass
        else:
            url = "https://www.books.ru/"
            response = requests.get(url, cookies=self.cookie_dict)
            with open(HTML_FILE, mode="w") as file:
                file.write(response.text)

        logger.info("OK | Файлы проверены")
    
    # Парсинг только сайт books.ru
    # Позже будет добавлена функция парсинга данных со страницы с сотнями книг (Этот сайт)


    # Функция для парсинга книг со скидкой
    def parse_html_file_sellers(self):
        with open("../html/sellers.html", mode="r", encoding="utf-8") as file:
            self.html_doc = file.read()

        soup = BeautifulSoup(self.html_doc, "html.parser")
        p = soup.find('div', "book-catalog_item")
        i = 0
        while p is not None:
            i+=1 
            name_books = p.find("a", "custom-link book-catalog_item_title")
            type_books = p.find("a", "viewed-items-book books viewed-items-book-card")

            price_books = p.find("div", "book-catalog_item_price-wrap")
            price = price_books.find("span", "book-price")
            author_books = p.find("a", "")

            if name_books is not None:
                name = name_books.string
            else:
                name = "None"

            if type_books is not None:
                type = type_books.string
            else:
                type = "None"

            if price is not None:
                price_n = price.get_text().split()
            else:
                price_n = "None"

            if author_books is not None:
                author = author_books.get_text()
            else:
                author = "None"

            self.books.books.append((name, type, author, price_n[0], price_n[1]))
            #print_books(name, author, type, price_n, i) Для вывода красивого
            p = p.find_next('div', "book-catalog_item")


    def parse_html_file(self):

        with open(HTML_FILE, mode="r", encoding="utf-8") as file:
            self.html_doc = file.read()

        soup = BeautifulSoup(self.html_doc, "html.parser")
        p = soup.find('div', "book-catalog_item")
        i = 0
        while p is not None:
            i+=1 
            name_books = p.find("a", "custom-link book-catalog_item_title")
            type_books = p.find("a", "viewed-items-book books viewed-items-book-card")

            price_books = p.find("div", "book-catalog_item_price-wrap")
            price = price_books.find("span", "book-price")
            author_books = p.find("a", "")

            if name_books is not None:
                name = name_books.string
            else:
                name = "None"

            if type_books is not None:
                type = type_books.string
            else:
                type = "None"

            if price is not None:
                price_n = price.get_text().split()
            else:
                price_n = "None"

            if author_books is not None:
                author = author_books.get_text()
            else:
                author = "None"

            self.books.books.append((name, type, author, price_n[0], price_n[1]))
            #print_books(name, author, type, price_n, i) Для вывода красивого
            p = p.find_next('div', "book-catalog_item")

    def update_html(self):
        url = "https://www.books.ru/"
        response = requests.get(url, cookies=self.cookie_dict)
        with open(HTML_FILE, mode="w") as file:
            file.write(response.text)
        logger.info("ОК | HTML обновлен")

    def parse(self, conn):
        self.check_files()
        if(self.update_html_bool):
            self.update_html()
        self.parse_html_file()
        for i in self.books.books:
            self.books.add(conn, i)
        logger.info("OK | Добавлены строки")
        logger.info("OK | Парсинг завершен")