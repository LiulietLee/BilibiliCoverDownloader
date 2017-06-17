from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import re, requests, sys
from bs4 import BeautifulSoup


#开始界面
def helloPage(request):
	return render(request ,'Downloader/helloPage.html')

#装载界面
def loadPage(request):

	url = "http://www.bilibili.com/video/" + request.POST['target']
	print(url)

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

	link = bs.findAll('img')[0].get('src')
	if link == None:
		return render(request, 'Downloader/resultPage.html')

	link = "http:" + link
	title = bs.findAll('h1')[0].get('title')
	contents = bs.findAll('meta')
	author = contents[3].get('content')
	
	print(link)
	print(title)
	print(author)
	return render(request, 'Downloader/loadPage.html', {'link':link, 'title':title, 'author':author})

#结果界面
def rusultPage(request):
	return HttpResponse("now you can see the Cover!")


