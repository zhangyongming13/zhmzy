# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
from zhmzy.settings import  DEFAULT_REQUEST_HEADERS, Header
import threading
from scrapy.conf import settings
import pymongo


class MyThread(threading.Thread):  # 重写多进程的方法，使其可以返回调用函数返回的数据
    def __init__(self, func, args, tiezi_link):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.tiezi_link = tiezi_link
        self.result = self.func(*self.args, self.tiezi_link)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def Get_tupian_data(src, tiezi_link):  # 获取图片链接对应的数据
    s = requests.session()
    # s.keep_alive = False
    header = Header
    header['Referer'] = tiezi_link[0]
    # print(DEFAULT_REQUEST_HEADERS)
    # print(header)
    req = s.get(src, headers=header)
    return req.content


class ZhmzyPipeline(object):

    def __init__(self):  # 初始化mongodb的数据库链接
        host = settings["MONGODB_HOST"]
        port = settings["27017"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data_mongodb = dict(item)  # 写入数据到mongodb数据库
        self.post.insert(data_mongodb)

        # 进行图片的获取还有写入本地磁盘
        dir_name = item['tiezi_name']
        if not os.path.exists(dir_name):  # 创建每个帖子对应的图片存放文件夹
            os.mkdir(dir_name)
        else:  # 已经存在文件夹，所以数据已经保存过了
            return item
        tupian_link = item['tupian_link']
        tiezi_link = item['tiezi_link']
        threads = []
        all_data = []
        for each in tupian_link:
            all_data.append(Get_tupian_data(each, tiezi_link))
        # src_number = range(len(tupian_link))  # 图片链接的个数也就是图片的个数
        # for i in src_number:  # 穿件创建多个进程用来访问图片链接取得数据
        #     t = MyThread(Get_tupian_data, (tupian_link[i],), (tiezi_link,))
        #     threads.append(t)
        #     threads[i].start()
        # for i in src_number:
        #     threads[i].join()
        # all_data = []  # 将一个帖子的所有图片的链接保存到一个list中，方便一次性写入硬盘，减少IO的时间
        # for i in src_number:
        #     result = threads[i].get_result()
        #     if result != None:
        #         all_data.append(result)
        #     else:
        #         pass
        num = 1
        for each in all_data:  # 讲图片数据保存到硬盘中
            file_name = str(num)
            num = num + 1
            with open('{}//{}.jpg'.format(dir_name, file_name), 'wb') as f:
                f.write(each)
        return item
