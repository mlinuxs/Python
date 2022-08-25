from multiprocessing.dummy import Lock
import re
import requests
import random
import time

headers={
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0'
}

#source可以替换，github上有很多
source='https://github.com/roosterkid/openproxylist/blob/main/HTTPS_RAW.txt'

def get_proxies(source_url=source):
    print('Try get proxies from:',source_url)
    resp=requests.get(source_url,verify=False,headers=headers)
    if resp.status_code!=200:
        print('Request for source page failed!')
        raise Exception('Get proxies Failed!')
    resp.encoding='utf8'
    raws=re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,6})',resp.text)
    proxies=[]
    for r in raws:
        proxies.append('https://'+r)
    return proxies

def get_proxies_retry(retries=5):
    if retries:
        try:
            proxies= get_proxies()
            print('Get proxies:',len(proxies))
            return proxies
        except Exception as e :
            print('Get proxies failed!')
            print(e)
            print('Remain retry times: ',retries)
            retries-=1
            time.sleep(3)
            return get_proxies_retry(retries)
    else:
        raise Exception("Can not get proxies with retrying!")

#包裹成一个类，方便调用
class ProxyPool():
    def __init__(self,minimal=10) -> None:
        self.proxies=[]
                #多线程爬虫时，加个锁
        self._lock=Lock()
        self.minimal=minimal

    def pick_proxy(self):
            #选择proxy时，检查代{过}{滤}理池是否够用
        self._fill_pool()
        return random.choice(self.proxies)

    def remove_proxy(self,proxy):
        try:
            self.proxies.remove(proxy)
            print('Remove proxy:',proxy)
        except:
            print('Proxy has been removed!')

    def _fill_pool(self):
            #少于minimal个代{过}{滤}理时，更新代{过}{滤}理池
        if len(self.proxies)<self.minimal:
                    #加锁，防止同时重复调用
            self._lock.acquire()
            if len(self.proxies)<self.minimal:
                self.proxies=get_proxies_retry()
            self._lock.release()
