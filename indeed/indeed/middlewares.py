# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import sys
from scrapy import signals
import time
import scrapy
# useful for handling different item types with a single interface
import indeed.chrome_settings as ChromeSetting
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException


class SeleniumMiddleWare:
    # def __init__(self) -> None:
        # self.browser= ChromeSetting.WebDriver().driver_instance

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # print("start process request:" + request.url)
        try:
            self.browser.get(request.url)
            self.browser.set_page_load_timeout(100)
            time.sleep(0.5)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding="utf-8", status=200)
        except Exception as e:
            # self.browser.execute_script("window.stop()")
            self.browser.quit()
            print("loading time too long... close")
            raise scrapy.exceptions.CloseSpider(reason="driver problem")
            # raise scrapy.exceptions.CloseSpider("Close Chrome")

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        self.browser= ChromeSetting.WebDriver(spider.COOKIE_NUM).driver_instance
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self):
            self.browser.quit()