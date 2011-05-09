"""
v0.1beta
Scrapes a given 'url' for files of type 'extension' 
Opens the files and saves them in the same folder as the script
"""

import os
import urllib
import re
import string
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup

def main():
  url = "http://www.cs.cornell.edu/home/kleinber/"
  extension = ".pdf"
  print "Scraping url %s for files of type %s...\n"%(url, extension)
  soup = BeautifulSoup(urllib.urlopen(url))
  tags = soup.findAll('a', href=True)
  for tag in tags:
    link = tag['href']
    if "http:" not in link and extension in link: 
      fqURL = urljoin(url, link) 
      fileName = ("%s%s"%(re.sub('[%s]' % re.escape(string.punctuation), \
      '', tag.renderContents()),extension)).replace(" ","_").\
      lstrip("\n").lower().replace("\n","_")
      fileContents = (urllib.urlopen(fqURL))
      fp = open(fileName, "wb")
      fp.write(fileContents.read())
      fp.close()
      os.chmod(fileName, 0644)
      print "Saved %s..."%fileName

if __name__ == "__main__":
  main() 
