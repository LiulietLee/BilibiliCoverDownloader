from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from bs4 import BeautifulSoup

import requests
import json
import sys
import re

from .info import cookies


headers = {'User-Agent':'Mozilla/5.0'}
default = {'url':'error','title':'error','author':'error'}
default_json = json.dumps(default, ensure_ascii=False, indent=2)

#手工输入跳转
def helloPage(request):
	return render(request ,'Downloader/helloPage.html')

#图片结果界面
def loadPage(request):
	av_number = request.POST['target']
	info = spider(av_number)
	if info['url'] == "error":
		return render(request, 'Downloader/404Page.html')
	else:
		return render(request, 'Downloader/loadPage.html', info)

# ios端的API
def iosPage(request, number):
	av_number = "av" + number
	info = spider(av_number)
	info_json = json.dumps(info, ensure_ascii=False, indent=2) 
	return HttpResponse(info_json)

#从url直接跳转
def resultPage(request, number):
	av_number = "av" + number
	info = spider(av_number)
	if info['url']== "error":
		return render(request, 'Downloader/404Page.html')
	else:
		return render(request, 'Downloader/loadPage.html', info)

#爬取up主头像的iOS端API
def searchUpPage(request, up_name):
	url = 'https://search.bilibili.com/upuser?keyword=' + up_name
	r = requests.get(url, headers = headers)
	bs = BeautifulSoup(r.text, 'html5lib')
	up_infos = {'sum':0,'upusers':[]}
	for up in bs.findAll(attrs={'class': 'up-item'}):
		up_face = up.findAll('div')[0]
		name = up_face.a['title']
		img_url = 'https:' + up_face.a.img['data-src']
		up_info = up.findAll('div')[1].findAll('div')[2].findAll('span')
		video_num = re.findall("\d+",up_info[0].get_text())[0]
		fans_num = re.findall("\d+",up_info[1].get_text())[0]
		up_info = {
			'name':name,
			'video_num':video_num,
			'fans_num':fans_num,
			'img_url':img_url,
		}
		up_infos['sum'] = up_infos['sum'] + 1
		up_infos['upusers'].append(up_info)

	json_obj = json.dumps(up_infos, ensure_ascii=False, indent=2) 
	return HttpResponse(json_obj)
	
# 爬取图片的爬虫代码
def spider(av_number):

	url = "http://www.bilibili.com/video/" + av_number
	r = requests.get(url, headers = headers)
	bs = BeautifulSoup(r.text, 'html5lib')
	img_link = bs.findAll('img')[0].get('src')

	if img_link == None:
		info = default
	else:
		img_url = "http:" + img_link
		title = bs.findAll('h1')[0].get('title')
		contents = bs.findAll('meta')
		author = contents[3].get('content')
		info = {
			'url':img_url,
			'title':title,
			'author':author,
		}
	return  info

def fuckBilibili(request, av_number):

	url = 'http://www.bilibili.com/video/av' + str(av_number)
	try:
		r = requests.get(url, headers=headers, cookies=cookies, timeout=3)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
	except:
		return HttpResponse(default_json)
	bs = BeautifulSoup(r.text, 'html5lib')
	link = bs.find_all('img')[0].get('src')		
	if link == None:
		return HttpResponse(default_json)
	else:
		title = bs.find_all('h1')[0].get('title')
		contents = bs.find_all('meta')
		author = contents[3].get('content')
		info = {'url':'https:' + link, 'title':title, 'author':author,}
		info_json = json.dumps(info, ensure_ascii=False, indent=2)
		return HttpResponse(info_json)

def articleCover(request, cv_number):
	url = 'http://www.bilibili.com/read/cv' + str(cv_number)
	try:
		r = requests.get(url, headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
	except:
		return HttpResponse(default_json)
	bs = BeautifulSoup(r.text, 'html5lib')
	error = bs.find_all('div', class_='error')
	if len(error) == 0:
		js = bs.find_all('script')[0].text
		if js == None:
			return HttpResponse(default_json)
		else:
			info = {
				'url':js.split('"')[7],
				'title':js.split('"')[11],
				'author':js.split('"')[3]
			}
			info_json = json.dumps(info, ensure_ascii=False, indent=2) 
			return HttpResponse(info_json)
	else:
		return HttpResponse(default_json) 
