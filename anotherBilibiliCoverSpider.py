# -*- coding: utf-8 -*-
# @Author: li
# @Date:   2017-06-13 14:52:03
# @Last Modified by:   li
# @Last Modified time: 2017-06-13 15:14:28

import os
import re, requests, sys
from bs4 import BeautifulSoup

def main(av):
	url = 'http://www.bilibili.com/video/av' + av

	headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',
			'Cookie':'sid=ao8p7v84; UM_distinctid=15b7180b90f66-0f075e064d05ab-396c7807-1fa400-15b7180b91285; pgv_pvi=3513811968; fts=1492257914; finger=14bc3c4e; buvid3=835A244A-230C-4CF5-8FB3-E8C675EE8EA115577infoc; purl_token=bilibili_1497336042; pgv_si=s4574550016; CNZZDATA2724999=cnzz_eid%3D108963144-1492253091-%26ntime%3D1497334496',
			'Host':'www.bilibili.com',
			'Referer':'http://space.bilibili.com/3098214',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	}

	r = requests.get(url, headers = headers)
	bs = BeautifulSoup(r.text, 'html5lib')

	title = bs.title.text.split('_')[0]#视频标题
	print(title)
	link = 'http:' + bs.body.img['src']#封面选择

	tail = re.findall('.*(\.\w+)', link)[0]#图片扩展名
	pic = 'cover' + tail

	#保存图片
	r = requests.get(link)
	if r.status_code == 200:
		open(pic, 'wb').write(r.content)

if __name__ == '__main__':
	if len(sys.argv) != 2 :
		print('please input av num...')
	else :
		av = sys.argv[1]
		main(re.findall('\d+', av)[0])
