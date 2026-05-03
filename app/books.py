from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup

class Books():

    def __init__(self):
        self.listBooks = tuple()

    def htmlMain(self):
        with sync_playwright() as p:
            browser = p.firefox.launch()
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://www.books.ru/")
            page.wait_for_timeout(1000)

            cookies = context.cookies()
            browser.close()

            cookie_dict = {c['name']: c['value'] for c in cookies}
        import os.path
        if(os.path.exists("cookies/cookies.txt")):
            pass
        else:
            with open("cookies/cookies.txt", mode="w") as file:
                import json
                file.write(json.dumps(cookie_dict))

        if(os.path.exists("html/response.html")):
            pass
        else:
            url = "https://www.books.ru/"
            response = requests.get(url, cookies=cookie_dict)
            with open("html/response.html", mode="w") as file:
                file.write(response.text)
        


    def parseBestsellerPage(self):
        with open("html/bestseller.html", mode="r", encoding="utf-8") as file:
            self.html_bestseller = file.read()
        soup = BeautifulSoup(self.html_bestseller, "html.parser")
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
                price_n = price.get_text()
            else:
                price_n = "None"

            if author_books is not None:
                author = author_books.get_text()
            else:
                author = "None"

            print(f"Название: {name}\nАвтор: {author}\nТип: {type}\nЦена: {price_n}\n___{i}___")
            p = p.find_next('div', "book-catalog_item")

    def parseMainPage(self):
        with open("test/response.html", mode="r", encoding="utf-8") as file:
            self.html_main = file.read()
        soup = BeautifulSoup(self.html_main, "html.parser")
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
                price_n = price.get_text()
            else:
                price_n = "None"

            if author_books is not None:
                author = author_books.get_text()
            else:
                author = "None"

            print(f"Название: {name}\nАвтор: {author}\nТип: {type}\nЦена: {price_n}\n___{i}___")
            p = p.find_next('div', "book-catalog_item")