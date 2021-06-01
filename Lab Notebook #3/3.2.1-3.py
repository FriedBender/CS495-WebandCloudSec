from bs4 import BeautifulSoup
import requests as s

site = 'ac781f141f75f3d080021b4e004d0019.web-security-academy.net'


site_url = f'https://{site}'
login_url = f"https://{site}/login"
login_response = s.get(login_url)
csrf = BeautifulSoup(login_response.text,'html.parser').find('input', {'name':'csrf'})['value']

login_data = {
        'csrf': csrf,
        'username': 'wiener',
        'password': 'peter'
}

resp = s.post(login_url,data=login_data)

s.headers.update({'Origin':'https://semchuk2.com'})

details_url = f"https://{site}/accountDetails"
resp = s.get(details_url)

# View the response headers showing the Origin is echoed
print(resp.headers)

# Get the response containing the API key
print(resp.text)

