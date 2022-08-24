import urllib.request
import urllib.parse
import xlrd
import json
 
 
class Check():
    def choose(self):
        while True:
            cartype = input('='*25+'\n1 -- 查询小型轿车违章\n2 -- 查询大型汽车违章'+'\n3 -- 同时查询所有类型\n'+'='*25+'\n请输入数字按Enter键确认：\n\n')
            if cartype == '1':
                return '02'
            elif cartype == '2':
                return '01'
            elif cartype == '3':
                return '03'
            else:
                print('\n'+'┌'+'─'*11+'┐'+'\n│输入有误，请重新输入。│\n'+'└'+'─'*11+'┘\n')
 
 
    def check(self, hphm, engine, body, hpzl):
        self.hphm = hphm
        self.engine = engine
        self.body = body
        self.hpzl = hpzl
        url = 'https://sp0.baidu.com/5LMDcjW6BwF3otqbppnN2DJv/traffic.pae.baidu.com/data/query?city=dongguan&hphm=&hpzl=&engine=&body=&source=pc'
        data = {
        'hphm': self.hphm,
        'hpzl': self.hpzl,
        'engine': self.engine,
        'body': self.body,
        'source': 'pc',}
 
        data = urllib.parse.urlencode(data).encode('utf-8')
        response = urllib.request.urlopen(url,data)
        msgjson = json.loads(response.read())
                    
        if 'success' in msgjson['msg'] :
            if msgjson['data']['count'] == 0:
                print(hphm+'\t没有违章')
            else:
                print(hphm+'\t违章', msgjson['data']['count'],'次')
                while msgjson['data']['count'] > 0:
                    print('时间： ', msgjson['data']['lists'][msgjson['data']['count']-1]['time']+'\n'
                          '罚款： ', str(msgjson['data']['lists'][msgjson['data']['count']-1]['fine'])+'\n'
                          '扣分： ', str(msgjson['data']['lists'][msgjson['data']['count']-1]['point'])+'\n'
                          '处理： ', str(msgjson['data']['lists'][msgjson['data']['count']-1]['handled'])+'\n'
                          '类型： ', msgjson['data']['lists'][msgjson['data']['count']-1]['violation_type']+'\n'
                          '地址： ', msgjson['data']['lists'][msgjson['data']['count']-1]['address']+'\n')
                    with open(r'查询结果.txt','a+') as file:
                        file.write(f'{hphm}\t违章\n{"时间： ", msgjson["data"]["lists"][msgjson["data"]["count"]-1]["time"]}\n{"罚款： ", msgjson["data"]["lists"][msgjson["data"]["count"]-1]["fine"]}\n{"扣分： ", msgjson["data"]["lists"][msgjson["data"]["count"]-1]["point"]}\n{"处理： ", msgjson["data"]["lists"][msgjson["data"]["count"]-1]["handled"]}\n{"类型： ", msgjson["data"]["lists"][msgjson["data"]["count"]-1]["violation_type"]}\n{"地址： ", msgjson["data"]["lists"][msgjson["data"]["count"]-1]["address"]}\n')
                    msgjson['data']['count'] -= 1
 
         
        elif '输入参数不合法' in msgjson['msg']:
            print(hphm, msgjson['msg'])
            with open(r'查询结果.txt','a+') as file:
                file.write(f'{hphm}\t查询失败，请检查车辆信息！\n'+'-'*70+'\n')
 
        else:
            print(hphm+'\t查询失败。')        
 
 
    def run(self):
        hpzl = self.choose()
        if hpzl == '02':
            print('开始查询，请稍等...\n\n'+'-'*30)
            for i in range(1, sheet.nrows):
                self.check(sheet.cell_value(i,0), sheet.cell_value(i,1), sheet.cell_value(i,2), hpzl)
                print('-'*30)
            input('\n\n查询结束，按Enter键结束。')
 
        elif hpzl == '01':
            print('开始查询，请稍等...\n\n'+'-'*30)
            for i in range(1, sheet2.nrows):
                self.check(sheet2.cell_value(i,0), sheet2.cell_value(i,1), sheet2.cell_value(i,2), hpzl)
                print('-'*30)
            input('\n\n查询结束，按Enter键结束。')
 
        else:
            print('开始查询，请稍等...\n\n'+'-'*30)
            print('        小型轿车\n')
            for i in range(1, sheet.nrows):
                self.check(sheet.cell_value(i,0), sheet.cell_value(i,1), sheet.cell_value(i,2), '02')
                print('-'*30)
            print('\n\n        大型汽车\n')
            for i in range(1, sheet.nrows):
                self.check(sheet2.cell_value(i,0), sheet2.cell_value(i,1), sheet2.cell_value(i,2), '01')
                print('-'*30)
            input('\n\n查询结束，按Enter键结束。')
 
 
car = xlrd.open_workbook(r'car.xls')
sheet = car.sheet_by_name('小车')
sheet2 = car.sheet_by_name('大车')
 
check =Check()
check.run()