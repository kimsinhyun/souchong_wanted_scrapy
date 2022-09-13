import re
import os
import scrapy
import copy
import time
import hashlib
import datetime
from pprint import pprint
from html_text import extract_text

# what = ["data","python","java","backend","ai","c++"]
what = "data"

# place = "Korea"
country = "www"

class Spider(scrapy.Spider):
    name = 'indeed'
    page_num = 32
    
    # start_urls = [f"https://{country}.indeed.com/jobs?q={what}&sort=date&l=&start={page}" for page in range(215*10, 500 * 10,10)]
    # start_urls = [f"https://{country}.indeed.com/jobs?q={what}&sort=date&l=&start={page}" for page in range(0*10, 1000 * 10,10)]
    # start_urls = [f"https://www.indeed.com/jobs?q=data&sc=0kf%3Ajt(internship)%3B&start={page}&vjk=547fa69c5a112897" for page in range(5*10, 500 * 10,10)]
    def __init__(self, COOKIE_NUM=0,WHAT="data",START_PAGE=0):
        self.skill = "Python"
        self.place = "Korea"
        self.COOKIE_NUM = COOKIE_NUM
        self.WHAT = WHAT
        self.START_PAGE = int(START_PAGE)
        self.start_urls = [f"https://{country}.indeed.com/jobs?q={WHAT}&sort=date&l=&start={page}" for page in range(int(self.START_PAGE*10), 150 * 10,10)]
        # pid = os.getpid()
        # print(f"os.getpid = {pid}")
        print(f"COOKIE_NUM: {COOKIE_NUM}")
        print(f"WHAT: {WHAT}")
        print(f"START_PAGE: {START_PAGE}")
    def start_requests(self):
        for url in self.start_urls:
            # print("start scrapping : " + url)
            # time.sleep(5)
            time.sleep(1)
            try:
                yield scrapy.Request(url, callback=self.parse)
            except Exception as e:
                print("something wrong")
                print(e)
                raise scrapy.exceptions.CloseSpider()


    def parse(self, response):
        item = dict()
        # print("start parse")
        
        # job_post_details=response.xpath("//div[@class='j_joblist']/div[@class='e']")
        job_post_details=response.xpath('//a[@data-hide-spinner="true"]')
        Next_page_label = response.xpath('//a[@aria-label="Next Page"]')
        #마지막 페이지이면 stop (실제로 stop보다는 아무것도 return 하지 않음, 중단시키고 싶은데 아직 방법을 모르겠음)
        if(len(Next_page_label) == 0):
            Next_page_label = response.xpath('//a[@aria-label="Next"]')
            if(len(Next_page_label) == 0):
                print("Last Page! Stop Scraping")
                print(f"os.getpid = {os.getpid}")
                raise scrapy.exceptions.CloseSpider("Close Chrome")
        #다음 페이지가 존재하면
        else:
            # print(f"length of job_post_details: {len(job_post_details)}")
            for page_num, entry in enumerate(job_post_details):
                item['search_keyword'] = self.WHAT
                item["post_url"] = entry.xpath("./@href").get()
                item['job_title'] = extract_text(entry.get())
                item['company_location'] = extract_text(response.xpath(\
                    f'//*[@id="mosaic-provider-jobcards"]/ul/li[{page_num}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/span').get())
                
                if(item["post_url"].find("/rc/clk") != -1):
                    item["post_url"] = item["post_url"].replace("/rc/clk","https://www.indeed.com/viewjob")
                elif(item["post_url"].find("company") != -1):
                    item["post_url"] = item["post_url"].replace("/company/","https://www.indeed.com/viewjob?cmp=")
                
                yield scrapy.Request(item["post_url"],callback=self.parse_detail,meta={'item':copy.deepcopy(item)})

    def parse_detail(self,response):
        item = response.meta['item']
        item['company_name'] = extract_text(response.xpath('//*[@id="viewJobSSRRoot"]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/a').get())
        item['company_rating'] = extract_text(response.xpath('//div[@class="icl-Ratings-starsFilled"]/@style').get()).replace("width:", "").replace("px","")
        item['company_reviews'] = extract_text(response.xpath('//div[@class="icl-Ratings-count"]').get()).replace(" reviews", "").replace(",","")
        item['job_salary'] = extract_text(response.xpath('//span[@class="icl-u-xs-mr--xs attribute_snippet"]').get())
        item['job_salary_estimated_by_indeed'] = extract_text(response.xpath('//*[@id="salaryGuide"]/ul/li[2]/text()').get()).split(" is Indeed's")[0]
        item['job_contract_type'] = extract_text(response.xpath('//span[@class="icl-u-xs-mr--xs attribute_snippet"]').get())
        temp_benefits_list  = response.xpath('//span[@class="jobsearch-JobMetadataHeader-item  icl-u-xs-mt--xs"]').extract()
        item['benefits'] = self.parse_benefits(temp_benefits_list)
        item['job_description'] = extract_text(response.xpath('//*[@id="jobDescriptionText"]').get())
        temp_post_date = extract_text(response.xpath('//*[@id="hiringInsightsSectionRoot"]/p/span[2]').get())
        item['post_date'] = self.parse_date(temp_post_date)
        
        encoded_string = (item['job_title'] + item['post_url']).encode()
        hexdigest = hashlib.sha256(encoded_string).hexdigest()
        item['hash_id'] = hexdigest
        # pprint(item)
        yield item
        
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
    