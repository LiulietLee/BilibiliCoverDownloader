import urllib2
from bs4 import BeautifulSoup

upuser = raw_input('input: ')
videoUrl = 'https://search.bilibili.com/upuser?keyword=' + upuser
headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(videoUrl, None, headers)
html = urllib2.urlopen(req).read()

page = BeautifulSoup(html, "html.parser")
# print page.prettify()
for up in page.find_all(attrs={'class': 'up-item'}):
    upface = up.find_all('div')[0]
    name = upface.a['title']
    imgUrl = 'https:' + upface.a.img['data-src']
    upinfo = up.find_all('div')[1].find_all('div')[2].find_all('span')
    videoNum = upinfo[0].get_text()
    fansNum = upinfo[1].get_text()

    print 'UP: ' + name
    print videoNum
    print fansNum
    print 'image url: ' + imgUrl
    print '___________________________________________________________________________'
