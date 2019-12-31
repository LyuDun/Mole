from scrapy_mole import Redis
from scrapy_mole import get_urls
import scrapy


class Sephora_scrapy(scrapy.Spider):
    name = 'sephora'
    allowed_domains = ["sephora.com"]
    CURRENT_PAGE = 1

    def parse(self, response):
        for url in get_urls(index=1):
            yield scrapy.Request(url, callback=self.parse_url)

    def parse_url(self, response):
        item = ScrapyMoleItem()
        item['product_url'] = url
        str1 = response.selector.xpath(
            '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/h1/a/span/text()')
        str2 = response.selector.xpath(
            '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/h1/span/text()')
        item['product_name'] = str1 + str2
        item['product_img'] = response.selector.xpath(
            '//*[@id="tabItem_6wt_1_0"]/div/div/div/img')
        item['product_variation'] = response.selector.xpath(
            '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/span/text()[1,2,3]')
        button = response.css('a[class="css-squbya "]')
        if 1 == len(button):
            item['product_status'] = 'Y'
        else:
            item["product_status"] = 'N'
        print (item)
