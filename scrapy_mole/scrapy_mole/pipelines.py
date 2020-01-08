# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy_mole import Redis
from scrapy_mole import logging


class ScrapyMolePipeline(object):
    def process_item(self, item, spider):
        item["update_time"] = datetime.utcnow()
        return item
