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
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI','165.132.172.93'),
            mongo_db=crawler.settings.get('MONGO_DB','indeed_data_ver2'),
            account = crawler.settings.get('USERNAME','thwhd1'),
            passwd = crawler.settings.get('PWD','thwhd1')
        )

    def open_spider(self, spider):
        uri = 'mongodb://%s:%s@%s:27017/?authSource=admin' % (self.account, parse.quote_plus(self.passwd),self.mongo_uri)
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[self.mongo_db]
        
    def process_item(self, item, spider):
        collection = 'indeed_data'
        self.db[collection].insert_one(dict(item))
        return item
    
    def close_spider(self, spider):
        self.client.close()