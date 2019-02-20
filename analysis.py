# _*_ coding: utf-8 _*_
import pandas as pd
import re
import jieba.analyse
from collections import Counter
import sys
import time
import jieba.posseg as pseg
import keywords_new

user_id = 3833629134
f = open(str(user_id)+".txt", "r")
f1 = open("category_"+str(user_id)+".txt", "w")
f2 = open("express_"+str(user_id)+".txt", "w")
f3 = open("word_"+str(user_id)+".txt", "w")
f4 = open("name_"+str(user_id)+".txt", "w")
list1 = []
record = {}  # 记录命中信息
express = {}
name_set = {}
while True:
    line = f.readline().strip()
    if line:
        item = line.split(' ', 1)[1]
        ex_all = re.findall(u"\\[.*?\\]", item)
        if ex_all:
            for ex_item in ex_all:
                express[ex_item] = express.get(ex_item, 0) + 1
        for kw, keywords in keywords_new.keyword_dict.items():  # kw是大类
            flag = 0  # 大类命中的标志
            for key, keyword in keywords.items():  # key 是小类
                if flag == 1:
                    break
                for word in keyword:  # 小类关键词
                    match_flag = 1  # 列表中关键词全部命中的标志
                    for small_word in word:  # 关键词列表
#                        print small_word
                        match = re.search(re.compile(small_word, re.I), item)
                        if not match:
                            match_flag = 0
                            break
                    if match_flag == 1:  #命中了一个小类
                        record[kw] = record.get(kw, 0) + 1 # 单次记录
                        flag = 1
                        break
        item = re.sub("\\[.*?\\]", '', item)
        list = jieba.cut(item, cut_all = False)
        for ll in list:
            list1.append(ll)  # 分词
        seg_list = pseg.cut(item)
        for word, flag in seg_list:
            if flag == 'nr':
                name_set[word] = name_set.get(word, 0) + 1
    else:
        print("退出")
        break

count = Counter(list1)
for item in sorted(dict(count).items(), key=lambda d:d[1], reverse = True):
    if len(item[0]) >= 2 and item[1] >= 3:
        print(item[0],item[1], file=f3)

for key, keywords in sorted(record.items(), key=lambda d:d[1], reverse = True):
    print('提到', key, record[key], '次', file=f1)

for key, keywords in sorted(express.items(), key=lambda d:d[1], reverse = True):
    print('使用了', key, '表情', express[key], '次', file=f2)

for key, keywords in sorted(name_set.items(), key=lambda d:d[1], reverse = True):
    print('使用了', key, name_set[key], '次', file=f4)