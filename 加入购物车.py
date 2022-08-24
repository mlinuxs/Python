import requests, re, time,execjs,random
import urllib.parse
from urllib.parse import unquote

def get_sign(data):  ##如果方法失效,第一时间要检查JS文件
    with open('test.js', 'r', encoding='utf8') as f:
        jscode = f.read()
    sign = execjs.compile(jscode)
    sign1 = sign.call("sign", data)
    return sign1

def 获取参数():
    短链接 = input('请输入微信分享链接:')
    heard = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12A365 MicroMessenger/5.4.1 NetType/WIFI'
    }
    r = requests.get(短链接, headers=heard).text
    真实地址 = r[r.find("https://a.m.taobao.com/"):r.find("'", r.find("https://a.m.taobao.com/"))]
    tk = 短链接[短链接.find('=') + 1:]
    ID = 真实地址[真实地址.find('/i') + 2:真实地址.find('.htm')]
    price = 真实地址[真实地址.find('price=') + 6:真实地址.find('&', 真实地址.find('price='))]
    suid = 真实地址[真实地址.find('suid=') + 5:真实地址.find('&', 真实地址.find('suid='))]
    shareUniqueId = 真实地址[真实地址.find('shareUniqueId=') + 14:真实地址.find('&', 真实地址.find('shareUniqueId='))]
    ut_sk = 真实地址[真实地址.find('ut_sk=') + 6:真实地址.find('&', 真实地址.find('ut_sk='))]
    un = 真实地址[真实地址.find('un=') + 3:真实地址.find('&', 真实地址.find('un='))]
    spm = 真实地址[真实地址.find('spm=') + 4:真实地址.find('&', 真实地址.find('spm='))]
    sp_tk = 真实地址[真实地址.find('sp_tk=') + 6:真实地址.find('&', 真实地址.find('sp_tk='))]
    bc_fl_src = 真实地址[真实地址.find('bc_fl_src=') + 10:真实地址.find('&', 真实地址.find('bc_fl_src='))]
    short_name = 真实地址[真实地址.find('short_name=') + 11:真实地址.find('&', 真实地址.find('short_name='))]
    bxsign = 真实地址[真实地址.find('bxsign=') + 7:]
    heard = {
        'Referer': 'https://h5.m.taobao.com/',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12A365 MicroMessenger/5.4.1 NetType/WIFI'
    }
    时间戳 = str(int(time.time() * 1000))
    r = requests.get(
        'https://h5api.m.taobao.com/h5/mtop.taobao.baichuan.smb.get/1.0/?jsv=2.6.2&appKey=12574478&t=1641292896089&sign=e02e24da3b819b99a6d7344bb0c310a8&api=mtop.taobao.baichuan.smb.get&v=1.0&type=originaljson&dataType=jsonp&timeout=10000',
        headers=heard).cookies
    token = r['_m_h5_tk'][:r['_m_h5_tk'].find('_')]

    data = '{' + '"id":"{}","price":"{}","sourceType":"item","suid":"{}","shareUniqueId":"{}","ut_sk":"{}","un":"{}","share_crt_v":"1","un_site":"0","spm":"{}","sp_tk":"{}","bc_fl_src":"{}","cpp":"1","shareurl":"true","short_name":"{}","bxsign":"{}","sm":"{}","app":"weixin","detail_v":"3.5.0","exParams":"'.format(
        ID, price, suid, shareUniqueId, ut_sk, un, spm, sp_tk, bc_fl_src, short_name, bxsign,
        tk) + r'{\"id\":\"' + ID + r'\",\"price\":\"' + price + r'\",\"sourceType\":\"item\",\"suid\":\"' + suid + r'\",\"shareUniqueId\":\"' + shareUniqueId + r'\",\"ut_sk\":\"' + ut_sk + r'\",\"un\":\"' + un + r'\",\"share_crt_v\":\"1\",\"un_site\":\"0\",\"spm\":\"' + spm + r'\",\"sp_tk\":\"' + sp_tk + r'\",\"bc_fl_src\":\"' + bc_fl_src + r'\",\"cpp\":\"1\",\"shareurl\":\"true\",\"short_name\":\"' + short_name + r'\",\"bxsign\":\"' + bxsign + r'\",\"sm\":\"' + tk + r'\",\"app\":\"weixin\",\"appReqFrom\":\"detail\",\"container_type\":\"xdetail\",\"dinamic_v3\":\"true\",\"supportV7\":\"true\",\"ultron2\":\"true\"}","itemNumId":"' + ID + '","pageCode":"miniAppDetail","_from_":"miniapp"}'

    sign = get_sign(token + '&' + 时间戳 + '&12574478&' + data)
    url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.6.2&appKey=12574478&t={}&sign={}&api=mtop.taobao.detail.getdetail&v=6.0&ttid=202012%40taobao_h5_9.17.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data={}'.format(
        时间戳, sign, urllib.parse.quote(data))
    # 开始获取数据---------------------------------------------
    r = requests.get(url, headers=heard).text
    categoryId=re.findall(r'categoryId":"(.*?)"', r)[0]
    print(categoryId)
    sellerId=re.findall(r'sellerId\\\\\\":(.*?),', r)[0]
    print(sellerId)
    itemId=re.findall(r'&itemId=(.*?)\\', r)[0]
    print(itemId)
    return itemId,sellerId,categoryId


def generateUmidToken():
    umid_token = 'C' + str(int(time.time() * 1000))
    umid_token += ''.join(str(random.choice(range(10))) for _ in range(11))
    umid_token += str(int(time.time() * 1000))
    umid_token += ''.join(str(random.choice(range(10))) for _ in range(3))
    return umid_token

def 淘宝扫码登录():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    login_url = 'https://login.taobao.com/member/login.jhtml?allp=&wbp=&sub=false&sr=false&c_is_scure=&from=tbTop&type=1&style=&minipara=&css_style=&tpl_redirect_url=\
                              https%3A//www.taobao.com&popid=&callback=&is_ignore=&trust_alipay=&full_redirect=&need_sign=&sign=&timestamp=&from_encoding=&qrLogin=&keyLogin=&newMini2='
    getqr_login_url = 'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=tb&appkey=00000000&umid_token={}'
    checkqr_login_url = 'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken={}&defaulturl=https://www.taobao.com'
    session.headers.update(headers)
    # 设置session的代理IP,要不然异地登录会有风控
    # 携趣代理IP : 'http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid=81058&vkey=61EED4111009A8FE180173CE13E03E23&num=1&time=30&plat=1&re=0&type=0&so=1&ow=1&spl=1&addr=广东&db=1'
    #session.proxies = {'https':代理IP}
    umid_token = generateUmidToken()
    response = session.get(login_url)
    response = session.get(getqr_login_url.format(umid_token))
    response_json = response.json()
    if response_json['success']:
        xcode_url = response_json.get('url', '')
        lg_token = response_json.get('lgToken', '')
        print('复制此链接到某宝搜索进行登录:','https://login.m.taobao.com/qrcodeCheck.htm?lgToken={}&tbScanOpenType=Notification'.format(lg_token))
    else:
        raise RuntimeError('Fail to login, unable to fetch url of qrcode')
    session.headers.update({'Referer': 'https://login.taobao.com/member/login_unusual.htm?user_num_id=2979250577&is_ignore=&from=tbTop&style=\
                                             &popid=&callback=&minipara=&css_style=&is_scure=true&c_is_secure=&tpl_redirect_url=https%3A%2F%2Fwww.\
                                             taobao.com%2F&cr=https%3A%2F%2Fwww.taobao.com%2F&trust_alipay=&full_redirect=&need_sign=&not_duplite_str\
                                             =&from_encoding=&sign=&timestamp=&sr=false&guf=&sub=false&wbp=&wfl=null&allp=&loginsite=0&login_type=11&lang\
                                             =zh_CN&appkey=00000000&param=7nmIF0VTf6m%2Bbx8wuCmPLTEdh1Ftef8%2B5yUA%2FXNtAI%2FfMwadkeaCast40u2Ng0%2FC7Z75s\
                                             OSVLMugWTqKjJ7aA55JYIL%2FPDFJ7zaJhq9XSVUOX%2B1AxQatuIvw4TXGJm1VG4alZ2UohVAAt5WTLYbs5im077nTG%2BOkovORQNtMCEzWKM\
                                             e0xcuienFAhsBhC0V7qIYZJvPGOOEt0tORA8Fv1zYPuOkWEPDFsPwYG5xj4LTKNZt5HSRRHkviiPy9AJ9uC%2Bs7V%2FQ7b6K07YUG1fA3tFwAL\
                                             GnorSUXRdhcXUBBAt6IiyStIkWFWDgJEymOAXOS5RNGlO1EL5ppmpQas7BarrW2Krui4bxV81AJXyxLfnk3MOxI2dUNdO9VQNY0F6a6nk%2FCzUfR\
                                             0NfPRrIoXuZDn2N01A8q5XGrMlWmBCH5%2FSKz6%2F%2BrUx3%2FxQTYWmgV49rVSdtySIHip5PsrXHWXCbHqscdve540l5CUKTT7znsoL45pth%2FosxMUb649Yw1EPAq'})
    while True:
        response = session.get(checkqr_login_url.format(lg_token))
        response_json = response.json()
        # --扫码成功
        if response_json['code'] == '10006':
            # ----检查是否需要安全验证
            response = session.get(response_json.get('url', '') + '&umid_token={}'.format(umid_token))
            if response.url.find('login_unusual.htm') > -1:
                raise RuntimeError('Fail to login, your account requires security verification')
            uid, token = re.findall(r'uid=(.*?)&token=(.*?)&', response_json.get('url'))[0]
            username = unquote(uid.replace('cntaobao', ''))
            break
        # --二维码已经失效
        elif response_json['code'] == '10004':
            raise RuntimeError('Fail to login, qrcode has expired')
        # --正在扫码或其他原因
        elif response_json['code'] in ['10001', '10000']:
            pass
        time.sleep(1)

    cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
    print('[INFO]: Account -> %s, login successfully' % username)
    infos_return = {'username': username, 'uid': uid, 'token': token}
    infos_return.update(response_json)
    print(cookies_dict)
    return cookies_dict



cookies=淘宝扫码登录()
tb_token=cookies['_tb_token_']
tsid = cookies['t']
itemId,sellerId,categoryId=获取参数()  # https://m.tb.cn/h.fQxjOfl?tk=Igyd2bCwOtM
deliveryCityCode = input('请输入您当地的邮政编码:')#行政区划代码  比如汕头就是440500
skuId = input('请输入商品SKUID:') #'4440144444848'
heard = {'referer': 'https://detail.tmall.com/item.htm?&id={}&skuId={}'.format(itemId, skuId),
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
         }


抢购时间=input('请输入抢购时间:')
while True:
    print(type(抢购时间))
    r = requests.get('http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp').text
    时间戳=int(r[-16:-3])
    if int(抢购时间)<=时间戳:
        #ks = str(time.time() * 1000)
        ks =时间戳
        r = requests.get(
            'https://fbuy.tmall.com/cart/addCartItems.do?_tb_token_={}&add=%7B%22deliveryCityCode%22%3A{}%2C%22campaignId%22%3A0%2C%22from_etao%22%3A%22%22%2C%22umpkey%22%3A%22%22%2C%22items%22%3A%5B%7B%22itemId%22%3A%22{}%22%2C%22skuId%22%3A%22{}%22%2C%22iChannel%22%3A%22%22%2C%22quantity%22%3A1%2C%22serviceInfo%22%3A%22%22%2C%22extraAttribute%22%3A%7B%7D%7D%5D%7D&tsid={}&itemId={}&sellerId={}&categoryId={}&root_refer=&item_url_refer=&noAnim=true&_ksTS={}_787&callback=jsonp788'.format(
                tb_token, deliveryCityCode, itemId, skuId, tsid, itemId, sellerId, categoryId, ks), headers=heard,
            cookies=cookies)
        print(r.text)
        break
    print('时间未到,继续等待')
    time.sleep(0.5)