# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2017-08-24 10:53:01
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-09-30 09:26:40

from bs4 import BeautifulSoup
from info import cookies
import requests
import re
import os
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
		link = bs.find_all('img')[0].get('src')
		if link == None:
			print('这个视频不存在, 也有可能是会员的世界。')
			print('如果是会员的世界的话，你可以通过调用“fuck_vip_world”方法来解决这个问题。')
			print('并且注意检查cookies填写的是否合法。')
			return None
		else:
			title = bs.find_all('h1')[0].get('title')
			contents = bs.find_all('meta')
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

	def fuck_vip_world(self, avNumber, cookies):
		url = 'http://www.bilibili.com/video/av' + str(avNumber)
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, headers=headers, timeout=3, cookies=cookies)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
		except:
			print('无法与这个链接建立通讯')
		else:
			if r == None:
				return None
			else:
				info_dic = self.analysis(r)
				return info_dic



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
		for up in bs.find_all(attrs={'class': 'up-item'}):
			upface = up.find_all('div')[0]
			name = upface.a['title']
			imgUrl = 'https:' + upface.a.img['data-src']
			upinfo = up.find_all('div')[1].find_all('div')[2].find_all('span')
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

# 爬取直播界面的背景图片，并保存
class Xspider():

	def main(self, url):
		response = self.request(url)
		if response == None:
			print("没有获取到任何信息哦")
		else:
			soup = self.analysis(response)
			self.get_bg(soup, url)

	def request(self, url):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, timeout=5, headers=headers)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
		except:
			print("好可惜，无法与网页 %s 建立通讯 " % url.split('/')[-1])

	def analysis(self, response):
		soup = BeautifulSoup(response, 'lxml')
		return soup

	def get_bg(self, soup, url):
		name = url.split('/')[-1]
		# 这里的路径改成本机路径就可以使用了
		path = '/Users/li/Desktop/' + name + '.jpg'
		bg_info = soup.find('div', class_='bk-img w-100 h-100')
		if bg_info == None:
			print("这个页面被锁定了，里面没有信息")
		else:
			bg_link = bg_info['style'][22:-1]
			if bg_link[0] == '/':
				bg_link = 'https:' + bg_link
				try:
					headers = {'User-Agent':'Mozilla/5.0'}
					img = requests.get(bg_link, headers=headers)
					img.raise_for_status()
					with open(path, 'wb') as f:
						f.write(img.content)
						f.close()
						print('YES! 图片 %s 号已经被保存到桌面了' % name)
				except:
					print('啦咧？无法保存图片')
			else:
				print('这个图片是bilibili官方提供的，被跳过了 = = ')

class ArticelImageSpider():

	def request(self, url):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
		except:
			print('无法与这个链接建立通讯')

	def analysis(self, response):
		soup = BeautifulSoup(response, 'html5lib')
		error = soup.find_all('div', class_='error')
		if len(error) == 0:
			js = soup.find_all('script')[0].text
			if js == None:
				print('啊咧？没有诶!')
				return None
			else:
				return js.split('"')[7]
		else:
			print('这个链接并不存在')
			return None	

	def main(self, url):
		response = self.request(url)
		if response == None:
			return None
		else:
			img_url = self.analysis(response)
			return img_url


'''
下面是测试

首先你自己的账号要登陆在浏览器上，然后用chrome找出下面我们需要的这三个cookies。
对应填进去替换“XXX”就好了

'''



s = AVInfoSpider()
info = s.fuck_vip_world(avNumber=13240059, cookies=cookies)
print(info)

