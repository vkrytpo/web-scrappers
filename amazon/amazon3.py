from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import requests
import time


def get_amazon_link(book_title):
  url = 'https://www.google.com/search?q=amazon+novel+'+book_title
  print(url)

  url = Request(url)
  url.add_header('User-Agent', 'Mozilla/5.0')

  with urlopen(url) as f:
    data = f.readlines()

    page_soup = soup(str(data), 'html.parser')
    for line in page_soup.findAll('h3',{'class':'r'}):
      for item in line.findAll('a', href=True):
        item = item['href'].split('=')[1]
        item = item.split('&')[0]
        return item


def get_wiki_link(book_title):
  url = 'https://www.google.com/search?q=wiki+novel+'+book_title
  print(url)
  url = Request(url)
  url.add_header('User-Agent', 'Mozilla/5.0')

  with urlopen(url) as f:
    data = f.readlines()

    page_soup = soup(str(data), 'html.parser')

    for line in page_soup.findAll('h3',{'class':'r'}):
      for item in line.findAll('a', href=True):
        item = item['href'].split('=')[1]
        item = item.split('&')[0]
        return item


a = open('amazonlinks','w')
w = open('wikilinks','w')
with open('booklist') as b:
  books = b.readlines()

  for book in books:
    book_title = book.replace(' ','+')
    amazon_result = get_amazon_link(book_title)
    amazon_msg = book +'@'+ amazon_result
    a.write(amazon_msg + '\n')
    time.sleep(5)
    wiki_result = get_wiki_link(book_title)    
    wiki_msg = book +'@'+ wiki_result
    w.write(wiki_msg + '\n')
    time.sleep(5)
a.close()
w.close()
