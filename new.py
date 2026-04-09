from playwright.sync_api import sync_playwright
import requests

with sync_playwright() as p:
    browser = p.firefox.launch()
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://5ka.ru/catalog/skidki-nedeli--251C17046/")
    page.wait_for_timeout(5000)

    cookies = context.cookies()
    print(cookies)
    browser.close()

# преобразуем cookies
cookie_dict = {c['name']: c['value'] for c in cookies}

# используем в requests
url = "https://5ka.ru/api/catalog/v2/stores/35XY/categories/251C17046/products"

response = requests.get(url, cookies=cookie_dict)

print(response)