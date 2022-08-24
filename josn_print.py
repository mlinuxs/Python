import urllib.request
import urllib.parse
import xlrd
import warnings
 
import json
 
warnings.simplefilter("ignore")
 
 
 
url = 'https://sp0.baidu.com/5LMDcjW6BwF3otqbppnN2DJv/traffic.pae.baidu.com/data/query?cb=jQuery1102012268154905248219_1614675001322&city=dongguan&hphm=%E7%B2%A4SV900C&hpzl=02&engine=5391286&body=8092202&source=pc&_=1614675001338'
data = {
'cb': 'jQuery1102012268154905248219_1614675001322',
'city': 'shanghai',
'hphm': '粤S88888',
'hpzl': '01',
'engine': '888888',
'body': '888888',
'source': 'pc',
'_': '1614675001338'}
 
data = urllib.parse.urlencode(data).encode('utf-8')
 
response = urllib.request.urlopen(url,data)
 
html = json.loads(response.read()[43:-1])
 
print(html)