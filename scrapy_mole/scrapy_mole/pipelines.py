# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
from .ext import Redis, DB, logging

class ScrapyMolePipeline(object):
    def process_item(self, item, spider):
        item["update_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """UPDATE mole_product SET product_name = '%s', product_variation = '%s', product_status = '%s', update_time ='%s' WHERE product_url = '%s' """ % (
            item['product_name'], item['product_variation'],item['product_status'], item['update_time'], item['product_url'])
        with DB() as db:
            db.execute(sql)
