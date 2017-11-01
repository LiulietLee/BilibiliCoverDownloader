# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2017-10-10 15:09:01
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-11-01 10:22:40

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from bs4 import BeautifulSoup
import requests
import json
import sys
import re

from .models import Waifu2xData
from .info import cookies
from .logger import my_timer

headers = {'User-Agent': 'Mozilla/5.0'}
default = {'url': 'error', 'title': 'error', 'author': 'error'}
default_json = json.dumps(default, ensure_ascii=False, indent=2)


# 手工输入跳转
def helloPage(request):
    return render(request, 'Downloader/helloPage.html')


# 图片结果界面


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


# 从url直接跳转


def resultPage(request, number):
    av_number = "av" + number
    info = spider(av_number)
    if info['url'] == "error":
        return render(request, 'Downloader/404Page.html')
    else:
        return render(request, 'Downloader/loadPage.html', info)


# 爬取up主头像的iOS端API


@my_timer
def searchUpPage(request, up_name):
    url = 'https://search.bilibili.com/upuser?keyword=' + up_name
    r = requests.get(url, headers=headers)
    bs = BeautifulSoup(r.text, 'html5lib')
    up_infos = {'sum': 0, 'upusers': []}
    for up in bs.findAll(attrs={'class': 'up-item'}):
        up_face = up.findAll('div')[0]
        name = up_face.a['title']
        img_url = 'https:' + up_face.a.img['data-src']
        up_info = up.findAll('div')[1].findAll('div')[2].findAll('span')
        video_num = re.findall("\d+", up_info[0].get_text())[0]
        fans_num = re.findall("\d+", up_info[1].get_text())[0]
        up_info = {
            'name': name,
            'video_num': video_num,
            'fans_num': fans_num,
            'img_url': img_url,
        }
        up_infos['sum'] = up_infos['sum'] + 1
        up_infos['upusers'].append(up_info)

    json_obj = json.dumps(up_infos, ensure_ascii=False, indent=2)
    return HttpResponse(json_obj)


# 爬取图片的爬虫代码


@my_timer
def spider(av_number):
    url = "http://www.bilibili.com/video/" + av_number
    r = requests.get(url, headers=headers)
    bs = BeautifulSoup(r.text, 'html5lib')
    img_link = bs.findAll('img')[0].get('src')

    if img_link == None:
        pre_path = 'https://search.bilibili.com/all'
        kv = {'keyword': av_number}
        r = requests.get(pre_path, headers=headers, params=kv)
        bs = BeautifulSoup(r.text, 'html5lib')
        re_av_info_li = bs.findAll('li', class_='video list av')
        if len(re_av_info_li) is 0:
            info = {'url': 'error', 'title': 'error', 'author': 'error'}
        else:
            img_dic = re_av_info_li[0].findAll('a')[0].find('img').attrs
            re_img_link = 'http:' + img_dic['data-src']
            author = re_av_info_li[0].findAll('a')[-1].string
            title = re_av_info_li[0].findAll('a')[0].get('title')
            info = {
                'url': re_img_link,
                'title': title,
                'author': author,
            }
    else:
        img_url = "http:" + img_link
        title = bs.findAll('h1')[0].get('title')
        contents = bs.findAll('meta')
        author = contents[3].get('content')
        info = {
            'url': img_url,
            'title': title,
            'author': author,
        }
    return info


@my_timer
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
        info = {'url': 'https:' + link, 'title': title, 'author': author, }
        info_json = json.dumps(info, ensure_ascii=False, indent=2)
        return HttpResponse(info_json)


@my_timer
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
                'url': js.split('"')[7],
                'title': js.split('"')[11],
                'author': js.split('"')[3]
            }
            info_json = json.dumps(info, ensure_ascii=False, indent=2)
            return HttpResponse(info_json)
    else:
        return HttpResponse(default_json)

def waifu2xData(request):  
    try:
        iphone = request.GET.get('iphone')
        run_time = request.GET.get('time')
        img_len = request.GET.get('len')
        img_wid = request.GET.get('wid')
        img_area = str(float(img_len)*float(img_wid))
        status = {'status':'OK'}
    except:
        status = {'status':'ERROR'}
    else:
        data = Waifu2xData(iphone_type=iphone, run_time=run_time, img_len=img_len, img_wid=img_wid, img_area=img_area)
        data.save()
    status_json = json.dumps(status, ensure_ascii=False, indent=2)
    return HttpResponse(status_json)
