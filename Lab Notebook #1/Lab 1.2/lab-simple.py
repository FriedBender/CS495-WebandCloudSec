import requests
from bs4 import BeautifulSoup


def getUrlTitle(url):
  """
  This function returns the <title> of an HTML document given its URL
  :param url: URL to retrieve
  :type url: str
  :return: Title of URL
  :rtype: str
  """
  resp = requests.get(url)
  soup = BeautifulSoup(resp.text,'html.parser')
  title = str(soup.find('title'))
  return(title)

def getSequential(urls):
  """
  Given a list of URLs, retrieve the title for each one using a single synchronous process
  :param urls: List of URLs to retrieve
  :type urls: list of str
  :return: list of titles for each URL
  :rtype: list of str
  """
  titles = []
  for u in urls:
      titles.append(getUrlTitle(u))
  return(titles)

urls = ['https://pdx.edu', 'https://oregonctf.org']

print(getSequential(urls))