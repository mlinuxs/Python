import os

def listdir(path): #传入根目录
    print(path)
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file) #获取绝对路径
        if os.path.isdir(file_path): #如果还是文件夹，就继续迭代本函数
            listdir(file_path)
        elif os.path.splitext(file_path)[1] == '.xls' or os.path.splitext(file_path)[1] == '.xlsx': #判断文件是否是Excel文件
            file_list.append(file_path)
    return file_list #返回Excel文件路径列表


if __name__ == '__main__':
    path = r'D:\Code'
    file_list = listdir(path)
    for file_name in file_list:
        print('start translating',file_name)