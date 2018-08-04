# sample link to download from:
# http://libgen.io/search.php?req=Lecture+notes+on+computer+science&open=0&res=100&view=simple&phrase=1&column=def&sort=def&sortmode=ASC&page=1

import urllib.request
from bs4 import BeautifulSoup
import re
import os
import sys


# --------------------
# Necessary functions:
# --------------------


# returns search URLs in the required format:
def getSearchLink(searchTerm, pageNumber) :
  # replace all ' ' with '+':
  searchTerm = searchTerm.replace(' ', '+')
  pageNumber = str(pageNumber)

  string = 'http://libgen.io/search.php?req=' + searchTerm + '&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def&sort=def&sortmode=ASC&page=' + pageNumber
  # print(string)
  return string

# Returns the source code of the passed link:
def getPage(link) :
  attempts = 0
  while attempts <= 10 :
    if urllib.request.urlopen(link).getcode() != 200 :
      attempts += 1
    elif urllib.request.urlopen(link).getcode() == 200 :
      page = urllib.request.urlopen(link).read().decode()
      break

  if attempts < 10 :
    return page
  else :
    return -1


# ---------------------------
# Search, parse and download:
# ---------------------------


# if the folder 'books' does not exist, create it:
if not os.path.exists('books') :
  os.makedirs('books')

for pageNumber in range(1, 11) :
  searchLink = getSearchLink('Lecture notes on computer science', pageNumber)
  if searchLink != -1 :
    page = getPage(searchLink)
  else :
    sys.exit('\n\n\nCompleted parsing; no other pages found\n\n\n')
  soup = BeautifulSoup(page, 'html.parser')

  links = soup.findAll('a', href=re.compile('book/index.php'))

  count = 0

  for link in links :
    
    extension = link.parent

    count = 1
    while count <= 12 :
      extension = extension.nextSibling
      count += 1
    extension = extension.text
    
    print('\n' + link.text)

    # Go to the page to which the link goes :P
    bookSoup = BeautifulSoup(getPage('http://libgen.io/' + link['href']), 'html.parser')
    downloadPageLink = bookSoup.find('a', href=re.compile('^http://libgen.io/ads.php'))

    # Page that contains the download [GET] link
    downloadLinkSoup = BeautifulSoup(getPage(downloadPageLink['href']), 'html.parser')
    finalURL = downloadLinkSoup.find('h2').parent['href']
    print(finalURL)

    # Save to folder 'books':
    fileName = 'books/' + link.text.replace(':', '_') + '.' + extension
    urllib.request.urlretrieve(finalURL, fileName)