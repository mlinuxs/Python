def video(res, headers,date):
    vid = re.search(r'wxv_.{19}',res.text)
    # time.sleep(2)
    if vid:
        vid = vid.group(0)
        print('视频id',vid)
        url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&vid={vid}'
        data = requests.get(url,headers=headers,timeout=1).json()
        video_url = data['url_info'][0]['url']
        video_data = requests.get(video_url,headers=headers)
        print('正在下载视频：'+trimName(data['title'])+'.mp4')
        with open(date+'___'+trimName(data['title'])+'.mp4','wb') as f:
            f.write(video_data.content)
def audio(res,headers,date,title):
    aids = re.findall(r'"voice_id":"(.*?)"',res.text)
    time.sleep(2)
    tmp = 0
    for id in aids:
        tmp +=1
        url = f'https://res.wx.qq.com/voice/getvoice?mediaid={id}'
        audio_data = requests.get(url,headers=headers)
        print('正在下载音频：'+title+'.mp3')
        with open(date+'___'+trimName(title)+'___'+str(tmp)+'.mp3','wb') as f5:
            f5.write(audio_data.content)
url = input('请输入文章链接：')
response = requests.get(url, headers=headers)
urls = re.findall('<a target="_blank" href="(https?://mp.weixin.qq.com/s\?.*?)"',response.text)
urls.append(url)
print('文章总数',len(urls))

for mp_url in urls:
    res = requests.get(html.unescape(mp_url),proxies={'http': None,'https': None},verify=False, headers=headers)
    content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
    try:
        title = re.search(r'var msg_title = \'(.*)\'', content).group(1)
        ct = re.search(r'var ct = "(.*)";', content).group(1)
        date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
        print(date,title)
        audio(res,headers,date,title)
        video(res,headers,date)
        with open(date+'_'+title+'.html', 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as err:
        with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
            f.write(content)
