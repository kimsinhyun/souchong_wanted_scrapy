from distutils.spawn import spawn
import os
# from indeed import Spider
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from indeed.spiders.indeed import Spider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

COOKIE_NUM_LIST= [0,1,2,3,4,5,6,7,8] 
WHAT_LIST = ['data','Back-End','Front-End','Network','Game Developer','AI','computer vision','system engineer']

# for i in range(len(COOKIE_NUM_LIST)):
# for i in range(2):
#     os.system("scrapy crawl indeed -a COOKIE_NUM={COOKIE_NUM_LIST[i]} -a WHAT={WHAT_LIST[i]}")

# __init__(self, COOKIE_NUM=0,WHAT="data"):
settings = get_project_settings()
process = CrawlerProcess()
process.crawl(Spider, COOKIE_NUM=COOKIE_NUM_LIST[4],WHAT=WHAT_LIST[4])
process.start()