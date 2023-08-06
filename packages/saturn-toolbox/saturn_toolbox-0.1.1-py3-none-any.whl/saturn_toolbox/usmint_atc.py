import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

headers = Headers(os="mac", headers=True).generate()
s = requests.Session()
#Sets the header and sets the session
def start():
    product_url = input('What is the url of the product? ')
    scrape_product = s.get(product_url, headers=headers).text
    soup1 = BeautifulSoup(scrape_product, 'lxml')
    product_id = soup1.find('input', {"id": "pid"})
    atc_link = f"https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-MiniAddProduct?pid={product_id.get('value')}"
    print('Your atc link is:', atc_link)