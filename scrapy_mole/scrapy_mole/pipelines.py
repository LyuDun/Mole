# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
from datetime import datetime
import pytz
from .ext import Redis, DB, logging

class ScrapyMolePipeline(object):
    def process_item(self, item, spider):
        item["update_time"] = datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S') 
        sql = """UPDATE mole_product SET product_name = '%s', product_variation = '%s', product_status = '%s', update_time ='%s' WHERE product_url = '%s' """ % (
            item['product_name'], item['product_variation'],item['product_status'], item['update_time'], item['product_url'])
        with DB() as db:
            print(sql)
            db.execute(sql)
