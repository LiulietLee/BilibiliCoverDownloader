# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2017-08-24 10:53:01
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-08-24 16:06:45

from bs4 import BeautifulSoup
import requests
import re
import json

class AVInfoSpider():

	def request(self, url):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, headers=headers, timeout=3)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r
		except:
			print('无法与这个链接建立通讯')

	def analysis(self, response):
		bs = BeautifulSoup(response.text, 'html5lib')
		link = bs.findAll('img')[0].get('src')
		if link == None:
			print('这个视频不存在')
			return None
		else:
			title = bs.findAll('h1')[0].get('title')
			contents = bs.findAll('meta')
			author = contents[3].get('content')
			dic = {'link':'https:' + link, 'title':title, 'author':author,}
			return dic

	def get_Info(self, avNumber):
		url = 'http://www.bilibili.com/video/av' + str(avNumber)
		response = self.request(url)
		if response == None:
			return None
		else:
			info_dic = self.analysis(response)
			return info_dic

	def get_cover_link(self, avNumber):
		info_dic = self.get_Info(avNumber)
		if info_dic == None:
			return None
		else:
			return {'link':info_dic['link']}

class LiveCoverSpider():

	def request(self, url, kv):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, params=kv, headers=headers, timeout=3)
			r.raise_for_status()
			r.encoding = 'utf-8'
			return r
		except:
			print('无法与这个链接建立通讯')

	def get_cover_link(self, room_id):
		pre_link = 'https://api.live.bilibili.com/AppRoom/index'
		kv = {
			'device':'phone',
			'platform':'ios',
			'scale':'3',
			'build':'10000',
			'room_id':str(room_id),
		}
		response = self.request(pre_link, kv)
		if response == None:
			return None
		else:
			info = json.loads(response.text)
			return info['data']['cover']

class UpInfoSpider():

	def request(self, url, kv):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, params=kv, headers=headers, timeout=3)
			r.raise_for_status()
			r.encoding = 'utf-8'
			return r
		except:
			print('无法与这个链接建立通讯')

	def analysis(self, response):
		bs = BeautifulSoup(response.text, 'html5lib')
		up_infos = {'sum':0,'upusers':[]}
		for up in bs.findAll(attrs={'class': 'up-item'}):
			upface = up.findAll('div')[0]
			name = upface.a['title']
			imgUrl = 'https:' + upface.a.img['data-src']
			upinfo = up.findAll('div')[1].findAll('div')[2].findAll('span')
			videoNum = re.findall("\d+",upinfo[0].get_text())[0]
			fansNum = re.findall("\d+",upinfo[1].get_text())[0]
			up_info = {
				'name':name,
				'video_num':videoNum,
				'fans_num':fansNum,
				'img_url':imgUrl,
			}
			up_infos['sum'] = up_infos['sum'] + 1
			up_infos['upusers'].append(up_info)
		return up_infos

	def get_top_20_up_info(self, user_name):
		pre_link = 'https://search.bilibili.com/upuser'
		kv = {
			'keyword':str(user_name)
		}
		response = self.request(pre_link, kv)
		if response == None:
			return None
		else:
			info = self.analysis(response)
			return info
