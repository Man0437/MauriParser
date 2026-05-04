from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from books import Books
from dataclasses import dataclass

import requests
import os.path

# Если кому понадобится, то удобный вывод для записей с отпаршеного html, аналог Books.list() с другим выводом
def print_books(name, author, type, price_n, i):
    print(f"Название: {name}\nАвтор: {author}\nТип: {type}\nЦена: {price_n}\n___{i}___")


class Parser():
    def __init__(self):
        # cookies - поля для куки, поле класса
        # browser - Браузер для работы, поле класса ?? Пока не поле класса
        # context - поле класса
    
        # Можно добавить еще поле для самого парсера, но я не знаю зачем

        self.books = Books()
        with sync_playwright() as p:
            self.browser = p.firefox.launch()
            self.context = self.browser.new_context()
            page = self.context.new_page()
            page.goto("https://www.books.ru/")
            page.wait_for_timeout(1000)
            cookies = self.context.cookies()
            self.browser.close()

        print("OK | Browser")
        self.cookie_dict = {c['name']: c['value'] for c in cookies}
        print("OK | Cookies")

    def checkfiles(self):
        if(os.path.exists("../cookies/cookies.txt")):
            pass
        else:
            with open("../cookies/cookies.txt", mode="w") as file:
                import json
                file.write(json.dumps(self.cookie_dict))

        if(os.path.exists("../html/response.html")):
            pass
        else:
            url = "https://www.books.ru/"
            response = requests.get(url, cookies=self.cookie_dict)
            with open("../html/response.html", mode="w") as file:
                file.write(response.text)

        print("OK | Checked files")
    
    def parsehtml(self):

        with open("../html/response.html", mode="r", encoding="utf-8") as file:
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

            self.books.list_books.append((name, type, author, price_n[0], price_n[1]))
            #print_books(name, author, type, price_n, i) Для вывода красивого
            p = p.find_next('div', "book-catalog_item")

    def parse(self, conn):
        self.checkfiles()
        self.parsehtml()
        for i in self.books.list_books:
            self.books.add(conn, i)
        print("OK | Добавлены строки")