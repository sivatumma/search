'''
Created on Jan 24, 2013

@author: Don
'''
import sys
import urllib
import urlparse

from bs4 import BeautifulSoup 


class URLs(urllib.FancyURLopener):
    version = 'Chrome Version 24.0.1312.56 m - Just a test program - Excuse for Not being clear'
    #    Using this as an instance variable so that each instance gets a separate set of URLs to check
    links = []
    #    Using this as static like thing so that a URL once visited should not be visited again.
    visited = {"http://python.org/":False}

def process(links, level):
    if level > 0:
        for link in links:
            print link
            if URLs.visited[link] == False:            
                urls = URLs()
                URLs.visited[link] = True
                print ''
                print 'Processing link : ',  link
                fileType = link.rsplit(".")
                if (fileType[len(fileType)-1] not in ('msi', 'exe', 'bz2')):
                    try:
                        page = urllib.urlopen(link)
                        text = page.read()
                        page.close()
                        soup = BeautifulSoup(text)
                        for tag in soup.findAll('a', href=True):
                            tag['href'] = urlparse.urljoin(link, tag['href'])
                            urls.links.append(tag['href'])
                            urls.visited[tag['href']] = False
                            print tag['href']
                        print urls.links
                        process(urls.links, level-1)
                    except:
                        print 'Looks there is a problem parsing this URL. There can be many reasons. But for now, skipping this and moving on to the next URL.'
                        continue
                else:
                    print 'URL is not an html related file. Not parsing this. Going on to next link. \n\n'

def main():
    # Giving a base URL as seed, and telling it to terminate after 3rd level of parsing.
    process(["http://python.org/"], 3)
    
#############################################################################

if __name__ == "__main__":
    main()
