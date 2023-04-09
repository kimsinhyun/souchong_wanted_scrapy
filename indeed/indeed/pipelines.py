# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
"""
mongoDB version
"""
# import pymongo
# from urllib import parse

# import pymongo
# from urllib import parse

# class NewPipeline_mongo:
#     def __init__(self, mongo_uri, mongo_db,account,passwd):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#         self.account = account
#         self.passwd = passwd
        
#     @classmethod
#     def from_crawler(cls, crawler):
#         #print(crawler.settings.get('USERNAME'))
#         ## 연구실 DB
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI','165.132.172.93'),
#             mongo_db=crawler.settings.get('MONGO_DB','wanted'),
#             account = crawler.settings.get('USERNAME','thwhd1'),
#             passwd = crawler.settings.get('PWD','thwhd1')
#         )
#         # 개인 VM DB
#         # return cls(
#         #     mongo_uri=crawler.settings.get('MONGO_URI','192.168.56.110'),
#         #     mongo_db=crawler.settings.get('MONGO_DB','wanted'),
#         #     account = crawler.settings.get('USERNAME','test'),
#         #     passwd = crawler.settings.get('PWD','test')
#         # )
#     def open_spider(self, spider):
#         uri = 'mongodb://%s:%s@%s:27017/?authSource=admin' % (self.account, parse.quote_plus(self.passwd),self.mongo_uri)
#         self.client = pymongo.MongoClient(uri)
#         self.db = self.client[self.mongo_db]
        
#     def process_item(self, item, spider):
#         collection = 'wanted'
#         self.db[collection].insert_one(dict(item))
#         return item
    
#     def close_spider(self, spider):
#         self.client.close()

"""
mariaDB version
"""

import pymysql
import pymysql.cursors

class NewPiplineMariaDB:
    def __init__(self, conn):
        self._conn = conn
        
    @classmethod
    def from_settings(cls, settings):
        conn = pymysql.connect(
                                host = settings['MARIADB_HOST'],
                                user = settings['MARIADB_USER'],
                                password = settings['MARIADB_PWD'],
                                db = settings['MARIADB_DBNAME'],
                                charset='utf8'
                               )
        return cls(conn)
    
    def process_item(self, item, spider):
        sql = """INSERT INTO wantedTest 
            (   
                job_title, 
                company_name,
                job_tags,
                company_city,
                job_posting_date,
                job_location,
                skill_stacks,
                post_like_num,
                job_main_work,
                job_qualifications,
                job_preference,
                hash_key
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (
                    str(item["job_title"]),
                    str(item["company_name"]),
                    str(item["job_tags"]),
                    str(item["company_city"]),
                    str(item["job_posting_date"]),
                    str(item["job_location"]),
                    str(item["skill_stacks"]),
                    str(item["post_like_num"]),
                    str(item["job_main_work"]),
                    str(item["job_qualifications"]),
                    str(item["job_preference"]),
                    str(item["hash_key"])
                )
        with self._conn.cursor() as cursor:
            cursor.execute(sql,values)
        self._conn.commit()
        return item
    
    def close_spider(self, spider):
        self._conn.close()
        
class SQLs:
    @classmethod
    def saveWholeData(cursor, item):
        sql = """INSERT INTO wantedTest 
            (   
                job_title, 
                company_name,
                job_tags,
                company_city,
                job_posting_date,
                job_location,
                skill_stacks,
                post_like_num,
                job_main_work,
                job_qualifications,
                job_preference,
                hash_key
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (
                    str(item["job_title"]),
                    str(item["company_name"]),
                    str(item["job_tags"]),
                    str(item["company_city"]),
                    str(item["job_posting_date"]),
                    str(item["job_location"]),
                    str(item["skill_stacks"]),
                    str(item["post_like_num"]),
                    str(item["job_main_work"]),
                    str(item["job_qualifications"]),
                    str(item["job_preference"]),
                    str(item["hash_key"])
                )
        with cursor:
            cursor.execute(sql,values)
        
    # @classmethod
    # def saveSKillStacks(cursor, item):
    #     for skill in item[]

        
        
        