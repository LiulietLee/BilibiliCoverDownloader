from django.test import TestCase
import json

from .logger import Logger

# Create your tests here.

class APITests(TestCase):

	def test_articleCover(self):

		urls = [
			'/ios/article/19009/',
			'/ios/article/16992/',
			'/ios/article/169922/',# error url
		]

		Logger.log_title('[test_articleCover]')
		self.base(urls)


	def test_fuckBilibili(self):

		urls = [
			'/ios/vip/13240059/',
			'/ios/vip/1699200000/',# error url
		]

		Logger.log_title('[test_fuckBilibili]')
		self.base(urls)

	def test_searchUpPage(self):

		urls = [
			'/ios/upuser-keyword=Lex/',
			'/ios/upuser-keyword=蕾丝/',
		]

		Logger.log_title('[test_searchUpPage]')
		self.base(urls)

	def test_iosPage(self):

		urls = [
			'/ios/7/',
			'/ios/100086/',
			'/ios/1/',# error url
			'/ios/15153636/'# bangumi av
		]

		Logger.log_title('[test_iosPage]')
		self.base(urls)
		
	def base(self, urls):

		for i, url in enumerate(urls):
			response = self.client.get(url)
			self.assertEqual(response.status_code, 200)
			r = json.loads(response.content.decode('utf-8'))
			info = json.dumps(r, indent=2, ensure_ascii=False,)
			Logger.log_response(info, i)
			

