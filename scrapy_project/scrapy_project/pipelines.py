# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib

class ScrapyProjectPipeline(object):
    def process_item(self, item, spider):
        url = item['url']
        file_name = hashlib.sha1(url).hexdigest()
        print("save to file: %s" % file_name)
        fp = open('result/'+file_name, 'w')
        fp.write(item['body'])
        fp.close()
        return item
