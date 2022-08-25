import os

import requests
from lxml import etree

def download_txt(name):
    params = {
        "keyword": name
    }
    host = "https://www.1biqug.com"
    resp = requests.get("https://www.1biqug.com/searchbook.php", params=params)
    html = resp.content.decode()
    html = etree.HTML(html)
    ret_list = html.xpath("//li/span[@class='s2']/a/@href")
    detail_url = host + ret_list[0]
    resp = requests.get(detail_url)
    html = etree.HTML(resp.content.decode())
    ret_list = html.xpath("//div[@id='list']//dd//a/@href")
    print(ret_list)
    if not os.path.exists("./{}".format(name)):
        os.mkdir("./{}".format(name))
    for ret in ret_list[12:]:
        url = host + ret
        resp = requests.get(url)
        info = resp.content.decode()
        html = etree.HTML(info)
        title = html.xpath("//h1/text()")
        path = os.path.join(name, title[0] + ".txt")
        path = path.replace("*", "")
        content = html.xpath("//div[@id='content']//text()")
        if os.path.exists("./{}/{}".format(name, title)):
            os.remove("./{}/{}".format(name, title))
        f_content = open(path, "a", encoding="utf-8")
        for con in content:
            if "chaptererror();" in con or "本站最新域名：" in con:
                break
            f_content.write(con + "\r\n")
        f_content.close()
        print(title[0])
    print(name, "下载完成了")

if __name__ == '__main__':
    story = input("请输入小说名：")
    download_txt(story)
