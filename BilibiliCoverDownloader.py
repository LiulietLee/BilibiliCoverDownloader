import urllib
import urllib2
from bs4 import BeautifulSoup

avNum = input('input av number: ')
videoUrl = "http://www.bilibili.com/video/av" + str(avNum) + "/"

values = { 'username': 'cqc', 'password': 'XXXX' }
headers = { 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Referer': videoUrl }
data = urllib.urlencode(values)
request = urllib2.Request(videoUrl, data, headers)
response = urllib2.urlopen(request)

page = BeautifulSoup(response, "html.parser")
imgLink = page.findAll('img')[0].get('src')
title = page.findAll('h1')[0].get('title')
contents = page.findAll('meta')
author = contents[3].get('content')

if imgLink != None:
    imgUrl = "http:" + imgLink
    print title
    print author
    print description
    print imgUrl
else:
    print "Cannot fetch url"
