import urllib2
import json

liveNum = input('input: ')
videoUrl = 'https://api.live.bilibili.com/AppRoom/index?device=phone&platform=ios&scale=3&build=10000&room_id=' + str(liveNum)
headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(videoUrl, None, headers)
data = urllib2.urlopen(req).read()

decoded = json.loads(data)
print 'room id: ' + str(decoded['data']['room_id'])
print 'title: ' + decoded['data']['title']
print 'up user: ' + decoded['data']['uname']
print 'cover image: ' + decoded['data']['cover']
