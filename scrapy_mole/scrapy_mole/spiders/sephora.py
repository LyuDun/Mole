import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy_mole.items import ScrapyMoleItem
import requests
import re


class Sephora_scrapy(RedisSpider):
    name = 'sephora'
    redis_key = 'sephora:start_urls'
    # https://www.sephora.com/product/detox-dry-shampoo-P378169?icid2=editors%27%20picks:p378169:product

    def __init__(self, *args, **kwargs):
        super(Sephora_scrapy, self).__init__(*args, **kwargs)

    def parse(self, response):
        item = ScrapyMoleItem()
        try:
            item['product_url'] = response.url
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

            url = response.url
            # 例如url:https://www.sephora.com/product/matte-velvet-skin-blurring-powder-foundation-P443566?skuId=2210052
            # 获取商品的编号

            pattern = re.compile(r"?<=P)\d+", url)
            product_no = pattern.search(url)
            # 获取商品具体型号的编号skuid, 如果获取不到：提取网页中的默认skuid
            pattern2 = re.compile(r"?<=skuId=)\d+", url)
            if skuId = pattern2.search(url):
                pass
            else:
                skuId = re.search(
                    r'/d+', response.selector.xpath('/html/head/script[51]').extract())
            # 拼接查是否有库存的api，请求api地址，解析json获取商品库存状态
            # https://www.sephora.com/api/users/profiles/current/product/P453916?skipAddToRecentlyViewed=false&preferedSku=2310324
            api_url = 'https://www.sephora.com/api/users/profiles/current/product/' + \
                str(product_no)

            header = {
                'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                'Referer' = url,
                'Host' = 'www.sephora.com'
            }
            api_response = requests.get(url=api_url, header=header)
            if api_response.status_code == '200':
                api_json = api_response.json
                for i in api_json['regularChildSkus']:
                    if i['skuId'] == skuId:
                        item['product_status'] = isAddToBasket = i['actionFlags']['isAddToBasket']
            yield item
        except Exception as e:
            print('error-----' + str(e))
