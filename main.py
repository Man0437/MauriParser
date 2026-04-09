import requests


url = "https://5ka.ru/api/catalog/v2/stores/35XY/categories/251C17046/products"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Connection": "keep-alive"
}

session = requests.Session()
session.headers.update(headers)
response = session.get(url)

print(response.status_code)

#data = response.json()
#
#for item in data.get("products", []):
#    name = item.get("name")
#    price = item.get("price", {}).get("value")
#    old_price = item.get("price", {}).get("old_value")
#
#    print(name, price, old_price)