
from bs4 import BeautifulSoup
import urllib.request
import requests
import shutil
import os
import time
import threading
control_time = 0

url=('https://phongvu.vn/')
protocol = url.split(':')[0]
html_text = requests.get(url).text

html_page = urllib.request.urlopen(url)
soup = BeautifulSoup(html_text, 'html.parser')
os.system("mkdir Image")
for img in soup.find_all('img'):
    link=(img.get('src'))
    if isinstance(link,str):
        if link[:4] != 'http':
            link = url[:-1] + link
        print(link)
        os.system("you-get "+str(link)+" -o Image")
exit()