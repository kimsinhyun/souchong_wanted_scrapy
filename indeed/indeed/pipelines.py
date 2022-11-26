# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from urllib import parse

import pymongo
from urllib import parse

class NewPipeline_mongo:
    def __init__(self, mongo_uri, mongo_db,account,passwd):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.account = account
        self.passwd = passwd
        
    @classmethod
    def from_crawler(cls, crawler):
        #print(crawler.settings.get('USERNAME'))
        ## 연구실 DB
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI','165.132.172.93'),
            mongo_db=crawler.settings.get('MONGO_DB','wanted'),
            account = crawler.settings.get('USERNAME','thwhd1'),
            passwd = crawler.settings.get('PWD','thwhd1')
        )
        # 개인 VM DB
        # return cls(
        #     mongo_uri=crawler.settings.get('MONGO_URI','192.168.56.110'),
        #     mongo_db=crawler.settings.get('MONGO_DB','wanted'),
        #     account = crawler.settings.get('USERNAME','test'),
        #     passwd = crawler.settings.get('PWD','test')
        # )
    def open_spider(self, spider):
        uri = 'mongodb://%s:%s@%s:27017/?authSource=admin' % (self.account, parse.quote_plus(self.passwd),self.mongo_uri)
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[self.mongo_db]
        
    def process_item(self, item, spider):
        collection = 'wanted'
        self.db[collection].insert_one(dict(item))
        return item
    
    def close_spider(self, spider):
        self.client.close()