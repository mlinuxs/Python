from collections import Counter
from datetime import datetime
from random import sample
from urllib.parse import quote_plus  #搜索时，中文转英文
import difflib
import jieba
import json
import pypyodbc
import re
import requests
 
corpid = ''  ###########################企业微信 corpid
corpsecret = ''  #######################企业微信应用 corpsecret
appid = ''  ############################企业微信应用 appid

####id  来源  标题 网址  日期
####
####
 
str_now = datetime.now().strftime('%H:%M')
str_month = datetime.now().strftime('%Y-%m')  #('%Y-%m-%d')
 
send_count = 11  #推送n-1条
 
 
def data(sql, write=False):
    hot_data = 'E:/hots.mdb'
    conn = pypyodbc.connect(
        u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + hot_data)
    cursor = conn.cursor()
    cursor.execute(sql)
    if write:
        cursor.commit()  # 别忘了立即提交
    else:
        data = cursor.fetchall()
        cursor.close()
        return data
 
 
def similar_title(title, old_title_list, bili=False):  #相似度>n才算是重复标题
    if bili:
        return False  #如果是B站，则不匹配相似度
    return any(
        difflib.SequenceMatcher(None, title, old_title).quick_ratio() > 0.7
        for old_title in old_title_list)
 
 
def filter_str(s):  #过滤标题的特殊字符
    for _ in range(3):
        for d in r'!！？?.。-_&·`、、：;*/\\':
            s = s.replace(f'{d}{d}', d)
        for d in r'{}“”【】~●▲▼◆■★':
            s = s.replace(d, '')
    s = s.replace(' ', '')
    return s
 
 
def zhong_wen(s):  #提取中文字符作为标题关键词
    res = re.findall('[\u4e00-\u9fa5A-Za-z0-9.-]', s)
    return ''.join(res)
 
 
def save(hot_list):
    title, url, site_name = hot_list
    sql = f"insert into list (标题,网址,来源) values('{title}','{url}','{site_name}')"
    data(sql, True)
 
 
def recently_hots(isbili=False, days=10):  #B站不管日期，只认来源
    if isbili:
        sql = "select 网址 from list where 来源='bili'"
    else:
        sql = f"select 标题 from list where 日期>date()-{days}"  #默认查询5天前的数据 不管来源
    return {i[0] for i in data(sql)}
 
 
def send_wx(x):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}'
    r = requests.get(url, timeout=5)
    tokens = r.json()['access_token']
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={tokens}"
    data = {
        "touser": "@all",
        # "touser": 'wuxiaozhi',
        "msgtype": "text",
        "agentid": appid,
        "text": {
            "content": x
        },
        "safe": 0,
    }
    data = json.dumps(data)
    return requests.post(url, data=data, timeout=9).json()
 
 
def weibo():
    rjson = requests.get("https://weibo.com/ajax/side/hotSearch")
    rjson = rjson.json()['data']['realtime']
    hot_list = set()
    for i in rjson[:send_count]:
        if 'is_ad' in i:  #过滤广告
            continue
        title = i['note']
        new_title = quote_plus(title) if '%' in title else title  #防止%在网址里面转码出错
        url = f'https://s.weibo.com/weibo/{new_title}'
        hot_list.add((title, url))
    return hot_list
 
 
def hot_words(title_list):
    words = jieba.cut_for_search(title_list)
    true_words = [i for i in words if len(i.strip()) >= 2]
    sl = Counter(true_words)
    return [i for i in sl if sl[i] >= 5]
 
 
def baidu():
    rjson = requests.get('https://top.baidu.com/board?tab=realtime')
    rjson.encoding = 'utf-8'
    html = rjson.text
    if zhushi_re := re.findall('<!--s-data:(.*false})-->', html, re.S):
        txt_json = f'{zhushi_re[0]}'  #以文本存储在HTML里面的JSON
    datas = json.loads(txt_json)
    real_data = datas['data']['cards'][0]['content']
    hot_list = set()
    for i in real_data[:send_count]:
        title = i['word']
        if title[0] != '#' and title[-1] != '#':
            new_title = quote_plus(
                title) if '%' in title else title  #防止%在网址里面转码出错
            url = f'https://www.baidu.com/s?wd={new_title}'
            hot_list.add((title, url))
    return hot_list
 
 
def all_bili_list(ups):  #获取所有UP主的更新
    hot_list = set()
    for uid in ups:
        params = (
            ('mid', uid),
            ('ps', '30'),
            ('tid', '0'),
            ('pn', '1'),
            ('keyword', ''),
            ('order', 'pubdate'),
            ('jsonp', 'jsonp'),
        )
        rjson = requests.get('https://api.bilibili.com/x/space/arc/search',
                             params=params).json()
        for i in rjson['data']['list']['vlist']:
            play = i['play']  #播放
            danmu = i['video_review']  #弹幕
            comment = i['comment']  #评论
            title = i['title']
            bvid = i['bvid']
            url = f'https://www.bilibili.com/video/{bvid}'
            # 播放>，弹幕>,评论>
            if (play > (300 * 10000) or danmu > 3000
                    or comment > 2000) and url not in recently_hots(True):
                hot_list.add((f'{ups[uid]}：{title}', url))
    return hot_list
 
 
def bili():
    sql = '''
    select top 10 Uid,Nick
        from up
        where unlike=false
        order by rnd(id)
    '''  #随机抽取10个Up主
    ups = dict(data(sql))
    hots = all_bili_list(ups)
    # for i in hots:
    #     print(i)
    shu = 3  #推送条数
    return sample(hots, shu) if len(hots) >= shu else hots
 
 
def replace_hot_title(title):  #热词加括号
    hot_list = ' '.join(recently_hots(False, 1))
    hwords = hot_words(hot_list)
    for i in hwords:
        if i in title:
            title = title.replace(i, f'({i})')
    return title
 
 
def send_top_news(site_name, hot_list):
    if site_name == 'baidu':
        site = '百度'
    elif site_name == 'bili':
        site = 'B站'
    elif site_name == 'weibo':
        site = '微博'
 
    new_list = [f'【{site}】{str_now}']
    start_num = 1
    old_title_list = recently_hots()  #获取已存在的热词
 
    for i in hot_list:
        title, url = i
        title = filter_str(title)  #过滤一下标题的特殊字符
        new_title = zhong_wen(title)  #提取title中文作为关键词 防止写入时出错
 
        if site_name == 'bili' or not similar_title(
                title, old_title_list):  #B站的不判断相似标题
            save([new_title, url, site_name])  #标题，网址，来源写入数据库
            new_list.append(
                f'<a href="{url}">{chr(10101+start_num)} {replace_hot_title(title)}</a>'
            )  #把热词加上括号
            start_num += 1
 
    if len(new_list) > 1:
        new_txts = '\n\n'.join(new_list)  #连接新热词（排除已存在的老热词）
        if not all([corpid, corpsecret, appid]):
            print('企业微信应用的信息未填写完整，不发送，只展示')
            print(new_txts)
        else:
            send_wx(new_txts)
 
 
if __name__ == '__main__':
    print('爬取 bili ...')
    send_top_news('bili', bili())
 
    print('爬取 baidu ...')
    send_top_news('baidu', baidu())
 
    print('爬取 weibo ...')
    send_top_news('weibo', weibo())
