import requests
from bs4 import BeautifulSoup
from time_decorator_function import time_decorator
import multiprocessing
import matplotlib.pyplot as plt

import asyncio, requests_async

"""
def getUrlTitle(url):
  
  This function returns the <title> of an HTML document given its URL
  :param url: URL to retrieve
  :type url: str
  :return: Title of URL
  :rtype: str
  
  resp = requests.get(url)
  soup = BeautifulSoup(resp.text,'html.parser')
  title = str(soup.find('title'))
  return(title)


@time_decorator
def getSequential(urls):
  
  Given a list of URLs, retrieve the title for each one using a single synchronous process
  :param urls: List of URLs to retrieve
  :type urls: list of str
  :return: list of titles for each URL
  :rtype: list of str
  
  titles = []
  for u in urls:
      titles.append(getUrlTitle(u))
  return(titles)

@time_decorator
def getMulti(urls, num_processes):
    
    Given a list of URLs, retrieve the title for each one using a single synchronous process
    :param urls: List of URLs to retrieve
    :type urls: list of str
    :param num_processes: Number of processes to use
    :type num_processes: int
    :return: list of str
    :rtype: list of str
    
    p = multiprocessing.Pool(num_processes)
    titles = p.map(getUrlTitle, urls)
    p.close()
    return(titles)
"""

#urls = ['https://pdx.edu', 'https://oregonctf.org', 'https://google.com', 'https://facebook.com', 'https://repl.it', 'https://ubuntu.com', 'https://www.reddit.com', 'https://yandex.com', 'https://www.petco.com', 'https://www.wikipedia.org', 'https://stackoverflow.com', 'https://www.pcc.edu']

resp = requests.get('https://thefengs.com/wuchang/courses/cs495/urls.txt')
urls = resp.text.split('\n')[:50]

# concurrencies = [40, 30, 20, 10, 5, 2]
# elapsed = []

"""
print("\nTotal URLS:", len(urls),"\n")
elapsedSequentual = getSequential(urls)
print(f'\nElapsed Sequentual: {elapsedSequentual:0.2f} secs\n')

#concurrencies = [2, 5, 10, multiprocessing.cpu_count()]
for c in concurrencies:
    elapsedMulti = getMulti(urls, c)
    elapsed.append(elapsedMulti)
    print(f'Concurrencies: {c},    Fetch time: {elapsedMulti:0.2f} secs\n')
"""

"""plt.scatter(concurrencies, elapsed)
plt.title("semchuk2")
plt.xlabel("Number of Processes")
plt.ylabel("Retrieval Time")
plt.show()"""


async def agetUrlTitle(url):
    """
    This asynchronous function returns the <title> of an HTML document given its URL
    :param url: URL to retrieve
    :type url: str
    :return: Title of URL
    :rtype: str
    """
    resp = await requests_async.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    title = str(soup.find('title'))
    return(title)


async def async_main(urls):
    titles = [ agetUrlTitle(u) for u in urls ]
    return(await asyncio.gather(*titles))


@time_decorator
def getAsync(urls):
    """
    Given a list of URLs, retrieve the title for each one using a single synchronous process
    :param urls: List of URLs to retrieve
    :type urls: list of str
    :return: list of str
    """
    return(asyncio.run(async_main(urls)))

fetch_time = getAsync(urls)
print(f'Async version: {fetch_time:0.2f}')