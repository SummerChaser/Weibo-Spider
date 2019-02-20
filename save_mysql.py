#! -*- encoding:utf-8 -*-
"""
保存到mysql数据库

"""
import pymysql
pymysql.install_as_MySQLdb()

class SaveWeibo(object):
    def __init__(self,items):
        self.host='127.0.0.1'
        self.port=3306
        self.user='root'
        self.password='123456'
        self.db='weibo'
        self.run(items)

    def run(self,items):
        #创建连接
        conn=pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,db=self.db,charset='utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor
        cur = conn.cursor()
        params=[]
        for item in items:
            params.append((item.categoryName, item.middleUrl, item.bookName, item.wordsNums, item.updateTiems,item.authorName))

        sql="insert into weibo(categoryName,middleUrl,bookName,wordsNums,updateTiems,authorName) values(%s, %s, %s, %s, %s, %s )"
        try:
            # 执行SQL
            ret=cur.executemany(sql,params)
            conn.commit()   #提交
            print(u'添加成功，共添加%s 条数据' %str(ret))
        except  Exception as e:
            print(e)
            conn.rollback()
        cur.close() # 关闭游标
        conn.close()    # 关闭连接