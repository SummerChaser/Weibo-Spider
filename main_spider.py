# _*_ coding: utf-8 _*_

import sys
import os
from bs4 import BeautifulSoup  # BeautifulSoup为python 爬虫库
import requests  # 网络请求库
import time
from lxml import etree  # python解析库,支持HTML，XML，XPath解析
from urllib.request import urlretrieve  # 用于图片下载

from save_mysql import SaveWeibo

# 改成自己的user_id和cookie
#user_id = 5588873822
#user_id = 5683535288
user_id = 3895559674
#user_id =2708482131
#user_id =6214770042
cookie = {"Cookie": "_T_WM=e02ad3d3c986ae679f856969d2615c7c; WEIBOCN_WM=20005_0002; WEIBOCN_FROM=1110006030; ALF=1546783181; SCF=AklT7c-fUtvfqgLlbtFajLdDsHYIQkzhXIgcQJm01aPWRPkGUPlei-26PVsadgceHx2NLTp9_8_1FxhaoOOjFxM.; SUB=_2A25xDgyeDeRhGeNL41oZ9y3EyT6IHXVS8JTWrDV6PUNbktBeLRnekW1NSIn_u05r1duI83QlGozfXKgP-zoQ3sOv; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWoc2Rou4KWVfifqv2Znac05JpX5KzhUgL.Fo-f1hnRS0eReoz2dJLoIXzLxKqL1heLBoeLxK-L1K5L1heLxKMLBKML12zLxK-L1hnL1h5LxK.LBo2LB.eLxKML1-2L1hBLxK-L1KqLBoHxUf2t; SUHB=0tK6jnKDtoyg7O; SSOLoginState=1544191182; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803%26uicode%3D20000174 "}
url = 'http://weibo.cn/%d/profile?page=1'%user_id
# 获取初始url页面html内容，获取user_id和cookie（在返回的response header中）
html = requests.get(url, cookies = cookie).content
print ('user_id和cookie读入成功')

# html元素selector
selector = etree.HTML(html)
# 通过xpath获取该用户微博页面总数
pageNum = int(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

result = ""
word_count = 1  # 爬取的微博和图片数
image_count = 1
imgsrc_list = [] # 图片链接列表

print ('该用户微博页数 : ',pageNum)

times = 5
one_step = int(pageNum/times)
for step in range(times):
    if step < times - 1:
        i = int(step * one_step + 1)
        j = int((step + 1) * one_step + 1)
    else:
        i = int(step * one_step + 1)
        j = int(pageNum + 1)
    for page in range(i, j):
        try:
            # 目标页面 url
            url = 'http://weibo.cn/%d/profile?page=%d'%(user_id,page)
            print('正在爬取url : ',url)
            # 获取当前url页面微博内容
            lxml = requests.get(url, cookies = cookie).content
            selector = etree.HTML(lxml)
            # 获取该页面微博list
            content = selector.xpath('//span[@class="ctt"]')
            # 遍历每条微博
            for each in content:
                # 获取文本内容，加入result，记录条数
                text = each.xpath('string(.)')
                text = "%d: "%(word_count) +text+"\n"
                result = result + text
                word_count += 1
            print ('第%d页微博内容爬取完完成'%(page))

            # 把当前页面lxml实例化为soup对象
            soup = BeautifulSoup(lxml, "lxml")
            # 获取所有图片链接
            urllist = soup.find_all(class_='ib')
            # 遍历每个图片url,加入
            for imgurl in urllist:
                imgsrc = imgurl.get('src')
                imgsrc_list.append(imgsrc)
                image_count += 1
            print ('第%d页图片爬取完成，获得如下图片：\n%s'%(page,imgsrc_list))
        except:
            print ('第',page,'页发生错误')

        time.sleep(0.001)  # 爬取每页间隔时间
    print ('正在进行第', step + 1, '次停顿，防止访问次数过多')
    time.sleep(1)


try:
    # 打开文本存放文件，如果不存在则新建
    fo_txt = open(os.getcwd()+"/%d"%user_id+".txt", "w")
    result_path = os.getcwd() + '/%d' % user_id+".txt"
    print('微博内容文本存放路径为 :',result_path)
    fo_txt.write(result)  # 将结果写入文件
    print('爬取成功！\n该用户微博内容：\n\n%s\n文本存放路径为%s' % (result,result_path))

except:
    print ('微博文本内容保存失败')

if not imgsrc_list:
    print ('该用户原创微博中不存在图片')
else:
    # 图片存放文件夹路径
    picdir=os.getcwd()+'/weibo_image'+str(user_id)
    print(picdir)
    if os.path.exists(picdir) is False:
        os.mkdir(picdir)  # 若不存在则新建
    img_index = 1

    # 遍历图片
    for imgurl in imgsrc_list:
        # 图片本地存放路径
        img_path = picdir + '/%s.jpg' % img_index
        print('正在保存',img_path)
        # 将图片下载到本地
        urlretrieve(imgurl, img_path)
        img_index += 1
    print('该用户微博图片下载完成！共有%d张图片，存放文件夹为 %s'%(img_index,picdir))