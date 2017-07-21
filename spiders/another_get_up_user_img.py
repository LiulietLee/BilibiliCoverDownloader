# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2017-07-21 16:05:37
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-07-21 17:25:46
import requests
from bs4 import BeautifulSoup

up_user = input('input: ')
video_url = 'https://search.bilibili.com/upuser?keyword=' + up_user
headers = {
	'User-Agent' : 'Mozilla/5.0',
}

r = requests.get(video_url, headers = headers)
bs = BeautifulSoup(r.text, 'html5lib')

for up in bs.findAll(attrs={'class': 'up-item'}):
    upface = up.findAll('div')[0]
    name = upface.a['title']
    imgUrl = 'https:' + upface.a.img['data-src']
    upinfo = up.findAll('div')[1].findAll('div')[2].findAll('span')
    videoNum = upinfo[0].get_text()
    fansNum = upinfo[1].get_text()

    print ('UP: ' + name)
    print (videoNum)
    print (fansNum)
    print ('image url: ' + imgUrl)
    print ('_______________________________________________________________')