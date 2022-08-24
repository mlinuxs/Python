import datetime
from selenium.webdriver import Firefox
import time
# 自动化工具 淘宝 登录（自动 破解验证码）
#
#web=Chrome()
def down_load():
    web.get('https://www.taobao.com/')
    if web.find_element_by_link_text('亲，请登录'):

        web.find_element_by_link_text('亲，请登录').click()
        time.sleep(3)
        web.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()
        time.sleep(20)

        web.get('https://cart.taobao.com/cart.htm')
        time.sleep(3)
#需要记录当前购物车的时间戳
    # while True:
    #     now = datetime.datetime.now()


def buy(times):
    #死循环
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print('login success:', now)
        #购买误差不能超过一秒，加毫秒单位
        #时间对比，如果现在的时间达到我们设置的时间
        if now >= times:#可以购买，加一个死循环，保证能买到，买到就停
            while True:
                try:
                    if web.find_element_by_xpath('//*[@id="J_SelectAll1"]'):
                    #//*[@id="J_SelectAll2"]  //*[@id="J_SelectAll1"]
                        web.find_element_by_xpath('//*[@id="J_SelectAll1"]').click()
                        break
                except:
                    print('没找到啊')
            while True:
                try:
                    if web.find_element_by_link_text('结 算'):
                        web.find_element_by_link_text('结 算').click()
                        print('快付钱！！！')
                        break
                except:
                    pass
            # 提交订单
            # while True:
            #     try:
            #         if web.find_element_by_link_text('提交订单'):
            #             web.find_element_by_link_text('提交订单').click()
            #             new_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            #             print('抢到了，时间为：',new_now)
            #             break
            #     except:
            #         print('再搞一次哈')
            # time.sleep(0.01)
#web.get('https://cart.taobao.com/cart.htm')
if __name__ == '__main__':
    times = input('请输入你要抢购的时间 格式为2021-8-21 3:22:00.000000 ：')
    web = Firefox()
    down_load()
    buy(times)

