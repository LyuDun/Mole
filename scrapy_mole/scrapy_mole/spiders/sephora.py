import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy_mole.items import ScrapyMoleItem


class Sephora_scrapy(RedisSpider):
    name = 'sephora'
    redis_key = 'sephora:start_urls'
    # https://www.sephora.com/product/detox-dry-shampoo-P378169?icid2=editors%27%20picks:p378169:product

    def __init__(self, *args, **kwargs):
        super(Sephora_scrapy, self).__init__(*args, **kwargs)

    def parse(self, response):
        item = ScrapyMoleItem()
        try:
            str1 = response.selector.xpath(
                '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/h1/a/span/text()')
            str2 = response.selector.xpath(
                '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/h1/span/text()')
            item['product_name'] = str1 + str2
            item['product_img'] = response.selector.xpath(
                '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div[1]/div/div/div/img/@src').extract()
            variations = response.selector.xpath(
                '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/span/text()').extract()
            tmp = ''
            for variation in variations:
                tmp = tmp + variation
            item['product_variation'] = tmp
            
            button = response.selector.xpath('/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/button').extract()[0].replace('<', '').replace('>', '').replace('/', '')
            search_obj = re.search('Out of stock', button)
            if search_obj:
                item['product_status'] = 'N'
            else:
                item["product_status"] = 'Y'
            yield item
        except Exception as e:
            print('error-----' + str(e))
