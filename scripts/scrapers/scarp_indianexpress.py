from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import datetime
from ..utils import database

def getData(pageurl):
    session = requests.Session()
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    res = session.get(pageurl, headers=headers)
    bsObj = BeautifulSoup(res.text,"html.parser")

    title = bsObj.find("meta",{"itemprop":"headline"}).attrs['content']
    shortDesc = bsObj.find("meta",{"itemprop":"description"}).attrs['content']
    published_on = bsObj.find("meta",{"property":"article:published_time"}).attrs['content']
    published_on_dt = datetime.datetime.strptime(published_on, '%B %d, %Y %I:%M %p')
    content_div = bsObj.find("div",{"itemprop":"articleBody"})
    for s in content_div.findAll("script"):
        s.decompose()
    content = '';

    for x in content_div.findAll("p"):
        paragraph = x.get_text().strip()
        if(paragraph == '' or paragraph == 'For all the latest Opinion News, download Indian Express App'):
            continue
        content = content+"<p>"+x.get_text().strip()+"</p>\n\n"
 
    #saveEditorial(title, subtitle, content, author, news_paper, published_date, fetched_date, fetched_url)
    database.saveEditorial(title, shortDesc, content, None, 'IndianExpress', published_on_dt, None, pageurl)

def crawlIndianExpress():
    session = requests.Session()
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    res = session.get("http://indianexpress.com/section/opinion/editorials/", headers=headers)
    bsObj = BeautifulSoup(res.text,"html.parser")
    edi_urls = bsObj.find("div",{"class":"profile-container"}).findAll("h6")
    url_list = []
    for x in edi_urls:
        edi_url = x.find("a").attrs['href']
        url_list.append(edi_url)

    url_list = database.filterOutExistingURL(url_list)
    for x in url_list:
        getData(x)

crawlIndianExpress()
