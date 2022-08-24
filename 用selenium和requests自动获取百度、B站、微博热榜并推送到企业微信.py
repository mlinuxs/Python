import json
from datetime import datetime
from os import path
 
import emoji
import requests as req
from fake_useragent import UserAgent
from selenium import webdriver
# from urllib.parse import quote_plus  #搜索时，中文转英文
 
corpid = ''  #企业微信的 corpid
corpsecret = ''  #企业微信 corpsecret 
appid = ''  #企业微信 appid
 
tToday = datetime.now().strftime('%H:%M')
send_count = 11  #推送n-1条
 
 
def filter_str(s):  #过滤标题的特殊字符
    for i in range(3):
        for d in r'!！？?.。-_#￥$%&·`、、：;*/\\':
            s = s.replace(f'{d}{d}', d)
        s = s.replace(' ', '')
    return emoji.get_emoji_regexp().sub(r'', s.encode('utf8').decode('utf8'))
 
 
def get_with_se(site):  #百度和B站都通过selenium获取
    ua = UserAgent().random
    option = webdriver.ChromeOptions()
    #躲过webdriver检测1
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    #躲过webdriver检测2
    option.add_experimental_option('useAutomationExtension', False)
    # 防止selenium错误提示
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_argument('user-agent=' + ua)  #随机UA
 
    #加速运行
    option.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    option.add_argument('--disable-gpu')  # 规避bug
    option.add_argument('--hide-scrollbars')  # 隐藏滚动条
    option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
    option.add_argument('--headless')  #隐藏运行
 
    wd = webdriver.Chrome(options=option)
    wd.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument', {
            'source':
            'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })  #躲过webdriver检测3
    hot_list = []
    if site == 'bili':
        url = 'https://www.bilibili.com/v/popular/rank/all'
        wd.get(url)
        for i in range(1, send_count):
            url_cmd = f'//*[@id="app"]/div/div[2]/div[2]/ul/li[{i}]/div/div[1]/a'
            url = wd.find_element_by_xpath(url_cmd).get_attribute('href')
            title_cmd = f'//*[@id="app"]/div/div[2]/div[2]/ul/li[{i}]/div/div[2]/a'
            title = wd.find_element_by_xpath(title_cmd).text
            zuozhe_cmd = f'//*[@id="app"]/div/div[2]/div[2]/ul/li[{i}]/div/div[2]/div/a/span'
            zuozhe = wd.find_element_by_xpath(zuozhe_cmd).text
            hot_list.append([f'{zuozhe}：{title}', url])
    elif site == 'baidu':
        url = 'https://top.baidu.com/board?tab=realtime'
        wd.get(url)
        for i in range(1, send_count):
            title = wd.find_element_by_css_selector(
                f'.category-wrap_iQLoo:nth-child({i}) .c-single-text-ellipsis'
            ).text.strip()
            url = f'https://www.baidu.com/s?wd={title}'
            hot_list.append([title, url])
    wd.quit()
    return hot_list
 
 
def save(file, content):
    with open(file, 'w', encoding='gb2312') as f:
        f.write(content)
 
 
def load(file):
    with open(file, 'r', encoding='gb2312') as f:
        hot_list = f.readlines()
    return [i.strip() for i in hot_list]
 
 
def send_wx(x):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}'
    r = req.get(url, timeout=5)
    tokens = json.loads(r.text)['access_token']
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + tokens
    data = {
        "touser": "@all",
        "msgtype": "text",
        "agentid": appid,
        "text": {
            "content": x
        },
        "safe": 0,
    }
    data = json.dumps(data)
    return req.post(url, data=data, timeout=9).text
 
 
def weibo():
    response = req.get("https://weibo.com/ajax/side/hotSearch")
    data_json = response.json()['data']['realtime']
    n = 1
    hot_list = []
    for i in data_json:
        title = i['note']
        url = 'https://s.weibo.com/weibo?q=%23' + i['word'] + '%23'
        hot_list.append([title, url])
        n += 1
        if n == send_count: break  #满10条就不写入了
    return hot_list
 
 
def send_top(site_name, hot_list):
 
    if site_name == 'bili':
        site = 'B站'
    elif site_name == 'baidu':
        site = '百度'
    elif site_name == 'weibo':
        site = '微博'
 
    new_list = [f'【{site}】{tToday}']
 
    full_hots_list = []
    start_num = 1
    file = f'E:/Backup/脚本/txt/{site_name}.txt'
    if not path.exists(file): save(file, '')  #旧热词文件不存在，就新建一个
    old_hot = load(file)  #获取已存在的热词
    for i in hot_list:
        title, url = i
        title = filter_str(title)  #过滤一下标题的特殊字符
        full_hots_list.append(title)  #标题写入列表，之后再写入文本，方便下次对比
        if title not in old_hot:
            new_list.append(f'<a href="{url}">{start_num}. {title}</a>')  #标记新的
            start_num += 1
    new_txts = '\n\n'.join(new_list)  #连接新热词（排除已存在的老热词）
    save(file, '\n'.join(full_hots_list))  #存储hotlist，方便下次对比
    if len(new_list) > 1:
        send_wx(new_txts)
 
 
if __name__ == '__main__':
    send_top('bili', get_with_se('bili')[:send_count])
    send_top('baidu', get_with_se('baidu')[:send_count])
    send_top('weibo', weibo())
