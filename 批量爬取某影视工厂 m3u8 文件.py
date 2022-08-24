import requests
import re
import json
import base64
 
headers = {
    # 'Referer': 'https://www.ysgc.vip/vodplay/17287-2-1.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
}
 
 
# 获取视频的名称和视频的 m3u8 文件
def get_m3u8():
    # 用来存储 m3u8 地址
    video_path = 'd://desktop/数码宝贝' + '.txt'
    with open(video_path, 'w', encoding='utf-8') as fp:
        fp.write(' ')
    fp.close()
    qq = open(video_path, 'w', encoding='utf-8')
 
    # 用来存储所有集数的播放链接
    play_url = []
 
    session = requests.Session()
    # 通过循环来获取每个播放页面，55 指的是播放集数 ，vodplay  后面的 17287-2 是播放的位置，修改也就是修改这里
    for s in range(31, 40):
        lang_url = 'https://www.ysgc.vip' + f'/vodplay/17287-2-{s}.html'
        play_url.append(lang_url)
 
    # 通过循环来获取每一集的 m3u8 文件
    for i in play_url:
        # 获取视频名称
        video_name = (re.findall(r'<title>(.*?)免.*?</title>', (session.get(i).text))[0])
        # 获取 var play = {} 数据
        get_var_play = json.loads(re.findall(r'<script type="text/javascript">var player_aaaa=(.*?)</script>', (session.get(i).text))[0])
        # 获取视频真实播放链接，并直接获取该地址的源代码，这里的dplay ,要根据解析平台需要自己修改，例如某讯视频就得用qq
        video_url = session.get(f'https://www.ysgc.vip/static/player/dplayer.php?url={get_var_play["url"]}').text
        # 获取m3u8的加密地址
        m3u8_url = re.findall(r"var.*?urls.*?=.*?'(.*?)';", video_url)[0]
        # 解密地址，并通过切割获取到m3u8链接，最后删除后面的9位数，得到最终的结果
        m3u8_true_url = ('http:' + (((str(base64.b64decode(m3u8_url.encode()))).split(' ')[0]).split('https:')[1]))[:-9]
 
        # 写入文件
        qq.write(str(video_name) + ',' + str(m3u8_true_url) + '\n')
        print(str(video_name) + '   >>>>>>>>>>> 写入完成')
 
    session.close()
    qq.close()
 
 
get_m3u8()
