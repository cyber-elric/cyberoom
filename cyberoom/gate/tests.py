from django.test import TestCase
import urllib.request
import xml.etree.ElementTree


url = 'http://cn.bing.com/HPImageArchive.aspx?idx=0&n=1'
req = urllib.request.Request(url)
response = urllib.request.urlopen(req)
root = xml.etree.ElementTree.fromstring(response.read())
wallpaperURL = 'http://cn.bing.com' + root.find('image').find('url').text
print(wallpaperURL)
