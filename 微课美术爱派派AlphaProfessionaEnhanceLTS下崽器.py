from pickletools import int4
import requests
from threading import Thread
from queue import Queue
from time import perf_counter
import json
import os
 
print (">>>微课美术爱派派下崽器V0.2(゜▽゜*)♪<<<")

# 初始化
q = Queue()
n_threads = int(input (">>>设置下载线程数:"))
buffer_size = 1024

# 读取j数据
file = open('js数据.txt', 'r',encoding='utf-8') 
js = file.read()
dic = json.loads(js) 

# 把字典数据搞出来
dic1 = dic['data']['dataMsg']['imgs']
# 提取文件夹名
folderename = dic['data']['dataMsg']['title']

input (f">>>文件夹名:{folderename},回车└→开始:")

if not os.path.exists(folderename):
    os.mkdir(folderename)
    print (">>>创建文件夹成功!<<<")
else:
    print(">>>该文件夹已存在.无法创建<<<")


def download():
    global q
    while True:
        # 从队列中获取 url
        url = q.get()
        # 按块下载响应正文，而不是立即下载
        response = requests.get(url, stream=True)
        # 获取文件名
        filename = url.split("/")[-1]
        with open(filename, "wb") as f:
            for data in response.iter_content(buffer_size):
                # 将读取的数据写入文件
                f.write(data)
                
        print (">>>已完成",filename,"文件下载")
        # 完成了文件的下载
        q.task_done()

if __name__ == "__main__":

    dataimg  = []

    # 遍历列表
    for linian in dic1:
        #print (linian['img'])
        dataimg.append(linian['img'])

    # 统计一共多少文件
    num_ = len(dataimg)

    #修改当前工作目录
    os.chdir(f"./{folderename}")

    # 文件url列表
    urls = dataimg * n_threads

    # 下载全部文件时间
    t = perf_counter()

    # 用所有 url 填充队列
    for url in urls:
        q.put(url)
    # 启动线程
    for t in range(n_threads):
        worker = Thread(target=download)
        # 表示主线程结束时会结束的线程
        worker.daemon = True
        worker.start()
    # 等待队列为空
    q.join()

# 文件夹地址
path = './'
# 读取当前文件夹
files = os.listdir(path)
# 统计文件夹一共多少文件
num_jpg = len(files)  

# 下载报告
print (">>>下载报告:")
print (f">>>已成功下载{num_jpg}份文件,耗时{perf_counter() - t:.2f}s")
print (f">>>文件夹:{folderename},共{num_}份文件")

# 核对下载文件
if num_jpg == num_ :
    print (">>>已核对,全部文件下载完成!!!<<<")
    input (">>>回车└→退出:")

else:
    # 可能还有更详细的核对(咕咕~~)
    print (">>>部分文件下载失败,请注意核对<<<")
    input (">>>回车└→退出:")
