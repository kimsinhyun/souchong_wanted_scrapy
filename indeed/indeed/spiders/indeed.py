import re
import os
import scrapy
import copy
import time
import hashlib
import datetime
from pprint import pprint
from html_text import extract_text


class Spider(scrapy.Spider):
    name = 'indeed'
    page_num = 32
    
    def __init__(self, COOKIE_NUM=0,WHAT="data",START_PAGE=1):
                            # https://www.wanted.co.kr/wdlist?country=kr&job_sort=job.latest_order&years=-1&locations=all
        self.start_urls = [f"https://www.wanted.co.kr/wd/{page}" for page in range(1,99999)]  
        print(f"COOKIE_NUM: {COOKIE_NUM}")
        print(f"WHAT: {WHAT}")
        print(f"START_PAGE: {START_PAGE}")
    def start_requests(self):
        for url in self.start_urls:
            time.sleep(1)
            try:
                yield scrapy.Request(url, callback=self.parse)
            except Exception as e:
                print("something wrong")
                print(e)
                raise scrapy.exceptions.CloseSpider()

    def parse(self, response):
        item = dict()
        # ========================
        item['pageNum'] = response.request.url.split("/")[-1]
        item['job_title'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/section[2]/h2').get())
        if(item['job_title'] == None):
            return
        item['company_name'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/section[2]/div[1]/h6/a').get())
        item['job_tags'] = []
        job_tags = response.xpath('//div[@class="Tags_tagsClass__mvehZ"]/ul/li').extract()
        for t in job_tags:
            item['job_tags'].append(extract_text(t))

        company_city = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/section[2]/div[1]/span/text()[1]').get())
        skill_stacks = extract_text(response.xpath('//div[@class="JobDescription_JobDescription_skill_wrapper__9EdFE"]').get())
        post_like_num = response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/aside/div/header/div[3]/button[1]/span/text()').get()
        job_introduction = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[1]').get())
        job_main_work = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[2]').get())
        job_qualifications = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[3]').get())
        job_preference = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[4]').get())
        job_other_details = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[5]').get())
        
        item['company_city'] = company_city
        item['job_posting_date'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section[2]/div[1]/span[2]').get())
        item['job_location'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section[2]/div[2]/span[2]').get())
        item['skill_stacks'] = skill_stacks.split('\n') if skill_stacks != None else []
        item['post_like_num'] = post_like_num
        item['job_introduction'] = job_introduction.split('\n') if job_introduction != None else []
        item['job_main_work'] = job_main_work.split('\n') if job_main_work != None else []
        item['job_qualifications'] = job_qualifications.split('\n') if job_qualifications != None else []
        item['job_preference'] = job_preference.split('\n') if job_preference != None else []
        item['job_other_details'] = job_other_details.split('\n') if job_other_details != None else []
        item['total_desciption'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div').get())
        
        # item['page_source'] = response.body.decode('utf-8')
        encoded_string = (item['job_title'] + item['company_name'] + item['job_posting_date'] + item['total_desciption']).encode()
        hexdigest = hashlib.sha256(encoded_string).hexdigest()
        item['hash_key'] = hexdigest
        yield item
        # ========================

        # job_post_details=response.xpath('//div[@data-cy="job-card"]')
        # print(f"length of job_post_details: {len(job_post_details)}")
        # for page_num, entry in enumerate(job_post_details):
        #     item["post_url"] = "https://www.wanted.co.kr" + entry.xpath("./a/@href").get()
        #     yield scrapy.Request(item["post_url"],callback=self.parse_detail,meta={'item':copy.deepcopy(item)})

    # def parse_detail(self,response):
    #     item = response.meta['item']
    #     item['job_title'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/section[2]/h2').get())
    #     item['company_name'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/section[2]/div[1]/h6/a').get())
    #     item['job_tags'] = []
    #     job_tags = response.xpath('//div[@class="Tags_tagsClass__mvehZ"]/ul/li').extract()
    #     for t in job_tags:
    #         item['job_tags'].append(extract_text(t))

    #     company_city = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/section[2]/div[1]/span/text()[1]').get())
    #     skill_stacks = extract_text(response.xpath('//div[@class="JobDescription_JobDescription_skill_wrapper__9EdFE"]').get())
    #     post_like_num = response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/aside/div/header/div[3]/button[1]/span/text()').get()
    #     job_introduction = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[1]').get())
    #     job_main_work = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[2]').get())
    #     job_qualifications = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[3]').get())
    #     job_preference = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[4]').get())
    #     job_other_details = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section/p[5]').get())
        
    #     item['company_city'] = company_city
    #     item['job_posting_date'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section[2]/div[1]/span[2]').get())
    #     item['job_location'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section[2]/div[2]/span[2]').get())
    #     item['skill_stacks'] = skill_stacks.split('\n') if skill_stacks != None else []
    #     item['post_like_num'] = post_like_num
    #     item['job_introduction'] = job_introduction.split('\n') if job_introduction != None else []
    #     item['job_main_work'] = job_main_work.split('\n') if job_main_work != None else []
    #     item['job_qualifications'] = job_qualifications.split('\n') if job_qualifications != None else []
    #     item['job_preference'] = job_preference.split('\n') if job_preference != None else []
    #     item['job_other_details'] = job_other_details.split('\n') if job_other_details != None else []
    #     item['total_desciption'] = extract_text(response.xpath('//*[@id="__next"]/div[3]/div[1]/div[1]/div').get())
        
    #     item['page_source'] = response.body.decode('utf-8')
    #     encoded_string = (item['job_title'] + item['company_name'] + item['job_posting_date'] + item['page_source']).encode()
    #     hexdigest = hashlib.sha256(encoded_string).hexdigest()
    #     item['hash_key'] = hexdigest
    #     yield item
        
    def parse_benefits(self,temp_benefits_list):
        benefits_list = []
        for benefit in temp_benefits_list:
            benefits_list.append(extract_text(benefit))
        return benefits_list
    
    def parse_date(self,temp_post_date):
        if(temp_post_date.find("30+") > -1):
            post_date = datetime.datetime(1, 1, 1, 0, 0).strftime('%Y-%m-%d')
        elif(temp_post_date.find("ago") > -1):
            day_delta = [int(s) for s in re.findall(r'\b\d+\b', temp_post_date)][0]
            post_date = (datetime.datetime.today() - datetime.timedelta(days=day_delta)).strftime('%Y-%m-%d')
        else:
            post_date = datetime.datetime.today().strftime('%Y-%m-%d')
        return post_date
    