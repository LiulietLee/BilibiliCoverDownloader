from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

#开始界面
def helloPage(request):
	return render(request ,'Downloader/helloPage.html')

#装载界面
def loadPage(request):
	return HttpResponse("this page is just a springboard...")

#结果界面
def rusultPage(request):
	return HttpResponse("now you can see the Cover!")


