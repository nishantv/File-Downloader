"""
v0.1beta
Scrapes a given 'url' for files of type 'extension' 
If directory is passed as parm, saves the files in the specified dir, else defaults to "downloaded_files"
"""

import os
import urllib
import re
import string
import sys
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup


def main():
    try:
        url = sys.argv[1]
        ext = sys.argv[2]
    except IndexError:
        print 'Usage: python getPDFs.py <url> <extension> <output_dir (optional)>'
        print 'Example: python getPDFs.py google.com .html'
        sys.exit(-2)
    try:
        output_dir = sys.argv[3]
    except IndexError:
        output_dir = "downloaded_files"
    extension = '.' + ext if not ext[0] == '.' else ext
    download_files(url, extension, output_dir)


def download_files(url, extension, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        os.chmod(output_dir, 0777)
    print "Scraping url %s for files of type %s...\n" % (url, extension)
    soup = BeautifulSoup(urllib.urlopen(url))
    tags = soup.findAll('a', href=True)
    for tag in tags:
        link = tag['href']
        if "http:" not in link and extension in link: 
            fq_url = urljoin(url, link)
            file_name = ("%s%s" % (re.sub('[%s]' % re.escape(string.punctuation), '', tag.renderContents()),
                                   extension)).replace(" ", "_").lstrip("\n").lower().replace("\n", "_")
            file_contents = (urllib.urlopen(fq_url))
            file_name = os.path.join(output_dir, file_name)
            with open(file_name, "wb") as fp:
                fp.write(file_contents.read())
            os.chmod(file_name, 0644)
            print "Saved %s..." % file_name


if __name__ == "__main__":
  main() 
