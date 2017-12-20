# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import scrapy
from w3lib.html import remove_tags
from scrapy_project.items import ScrapyProjectItem

def _start_urls():
    _s = []
    # if you really want more, please make it larger as you see the limit from the site (2148)
    for i in range(21):
        _s.append("http://www.zimuku.cn/search?q=&ad=1&p=%d" % (i+1))
    return _s


class SubtitleSpider(scrapy.Spider):
    name = 'subtitle'

    allowed_domains = ["zimuku.net", "zimuku.cn"]
    start_urls = _start_urls()
    
    def parse(self, response):
        hrefs = response.selector.xpath('//div[contains(@class, "sublist")]/table/tbody/tr/td/a/@href').extract()
        
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        hrefs = response.selector.xpath('//li[contains(@class, "li dlsub")]/div/a/@href').extract()
        if hrefs:
            self.log("try to follow %s" % hrefs)
            url = response.urljoin(hrefs[0])
            yield scrapy.Request(url, callback=self.parse_file)

    def parse_file(self, response):
        body = response.body
        self.log("download url %s" % response.url)
        item = ScrapyProjectItem()
        item['url'] = response.url
        item['body'] = body
        return item

    
