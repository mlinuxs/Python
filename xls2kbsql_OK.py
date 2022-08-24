import os,xlrd,json
import ksycopg2

#读取文件夹下面所有的xls文件
def listdir(path): #传入根目录
    for file in os.listdir(path):
        file_path = os.path.join(path, file) #获取绝对路径
        if os.path.isdir(file_path): #如果还是文件夹，就继续迭代本函数
            listdir(file_path)
        elif os.path.splitext(file_path)[1] == '.xls' or os.path.splitext(file_path)[1] == '.xlsx': #判断文件是否是Excel文件
            file_list.append(file_path)
    return file_list #返回Excel文件路径列表

#将读取的每一个xls文件插入数据库
def parse(file_path):
    conn = ksycopg2.connect(database="Test", user="SYSTEM", password="SYSTEM", host="127.0.0.1", port="54323")
    cur = conn.cursor()   
    file = xlrd.open_workbook(file_path)
    sheets = file.sheet_names()
    for i in sheets:
        sheet = file.sheet_by_name(i)
        row_num = sheet.nrows #获取行数
        for i in range(1, row_num):
            l = sheet.row_values(i)
            Snum = l[0]
            Score = l[1]
            sqlNonQuery = "insert into ql_ry (username,sfz) values ('%s',%d)" % (Snum, Score)
            print(sqlNonQuery)
            cur.execute(sqlNonQuery)
        conn.commit()

if __name__ == '__main__':
    file_list = []
    f = open('portal.txt', 'w', encoding='utf-8')
    path = r'C:\Users\mlinux\Desktop\xlss'
    #path = input("请输入文件夹路径: ")
    file_list = listdir(path)
    for file_name in file_list:
        print('start translating',file_name)
        #读取Excel所有的sheet到字典
        parse(file_name)

