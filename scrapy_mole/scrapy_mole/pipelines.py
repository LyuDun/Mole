# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import arrow
from scrapy_mole import Redis
from scrapy_mole import logging


class ScrapyMolePipeline(object):
    def process_item(self, item, spider):
        time = str(arrow.now().datetime())
        dict = {'product_url': item['product_url'],
                'product_name': item['product_name'],
                'product_img': item['product_img'],
                'product_variation': item['product_variation'],
                'product_status': item['product_status'],
                'update_time'： time
                }
        try:
            Redis.hmset(item['product_url'], dict)
        except Exception as e:
            logging.exception(e)
