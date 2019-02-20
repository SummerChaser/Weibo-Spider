# Weibo-Spider
#### python版本 : 3.7

####  简介 :
把main_spider中user_id和cookie改为自己的id和cookie。
打开微博手机版 https://m.weibo.cn/  

进入指定用户主页，如李荣浩的主页 : https://m.weibo.cn/u/1739046981?uid=1739046981&luicode=10000011&lfid=231093_-_selffollowed
其中1739046981就是用户id。

登录微博，进入个人主页，右键审查元素，切换到Network栏，勾选perserve log。
在左边name栏找到m.weibo.cn（或者其他能找到cookie）的url，从右边response header中找到COOKIE并复制粘贴到代码中。

![image.png](https://upload-images.jianshu.io/upload_images/1731341-c4ab83862e56f2b3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


main_spider.py 代码
```
# _*_ coding: utf-8 _*_

import sys
import os
from bs4 import BeautifulSoup  # BeautifulSoup为python 爬虫库
import requests  # 网络请求库
import time
from lxml import etree  # python解析库,支持HTML，XML，XPath解析
from urllib.request import urlretrieve  # 用于图片下载

# 改成自己的user_id和cookie
user_id = YOUR_ID
cookie = {"Cookie": "YOUR_COOKIE"}
# 初始url
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
```
运行截图 :
![image.png](https://upload-images.jianshu.io/upload_images/1731341-9bffecfa51325bd4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/1731341-04c7a5acdb891e9e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/1731341-1fb2fbbf24d63622.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

爬取的微博内容文件会被放到工程目录下用户对应的txt文件（自动生成）。
图片放到对应weibo_image文件下。

![image.png](https://upload-images.jianshu.io/upload_images/1731341-92c4801826a1dabd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/1731341-cb62a988c7e862e0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)













