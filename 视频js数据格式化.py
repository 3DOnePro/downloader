from cgi import print_environ_usage
import json

file = open('视频js数据.txt', 'r',encoding='utf-8') 
js = file.read()
dic = json.loads(js)   

# 输出字典
#print(dic) 

# 把字典搞出来
dic1 = dic['data']['msg']['file']
dic2 = dic['data']['msg']['video_name']
print (dic1)
print (dic2)
