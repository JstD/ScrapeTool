from bs4 import BeautifulSoup
import urllib.request
import re
import html2text
import pdfkit 


def not_relative_uri(href):
    if re.compile('^https://').search(href):
        return True
    return False
h = html2text.HTML2Text()
# Ignore converting links from HTML
h.ignore_links = True
url =  'https://vnexpress.net'

page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

new_feeds = soup.find_all()
for feed in new_feeds:
#     title = feed.get('title')
#     link = feed.get('href')
#     pdfkit.from_url(str(link),'1.pdf')
    # if not_relative_uri(link):
    #     print('Title: {} - Link: {}'.format(title, link))
    # print(h.handle(str(feed)),end='')
    print(feed)