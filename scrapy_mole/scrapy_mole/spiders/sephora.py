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
            print(item['product_url'])
            
            item['product_name'] = response.selector.xpath('/html/head/title/text()').extract_first()
        except Exception as e:
            print('name' + str(e)) 

            ''' 
            try:
                item['product_img'] = response.selector.xpath('/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div[1]/div/div/div/img/@src').extract_first()
            except Exception as e:
                print('img' + str(e)) 
            print(item['product_img'])
            '''
        try:
            variations = response.selector.xpath('//span[@data-comp="ProductVariation Text Box "]/text()').extract()
            tmp = ''
            for variation in variations:
                tmp = tmp + variation
            item['product_variation'] = tmp 
        except Exception as e:
            print('variation' + str(e)) 


        url = response.url
        # 例如url:https://www.sephora.com/product/matte-velvet-skin-blurring-powder-foundation-P443566?skuId=2210052
        # 获取商品的编号
        pattern = re.compile(r"(?<=P)\d+")
        product_no = pattern.search(url).group(0)
        # 获取商品具体型号的编号skuid, 如果获取不到：提取网页中的默认skuid
        try:
            pattern2 = re.compile(r"(?<=skuId=)\d+")
            m = pattern2.search(url)
            if m is not None:
                skuId = m.group(0)
            else:
                skuId_list = response.xpath('//div[@data-comp="SizeAndItemNumber Box "]/text()').extract()
                for skuId_str in skuId_list:
                    m  = re.search(r'\d{4,8}', skuId_str) 
                    if m is not None:
                        skuId = m.group(0)
                        break
        except Exception as e:
            print('skuId' + str(e))
        print('id是:'+ str(skuId)) 
        # 拼接查是否有库存的api，请求api地址，解析json获取商品库存状态
        # https://www.sephora.com/api/users/profiles/current/product/P453916?skipAddToRecentlyViewed=false&preferedSku=2310324
        api_url = 'https://www.sephora.com/api/users/profiles/current/product/P' + str(product_no)

        print(api_url)
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Referer' : url,
            'Host' : 'www.sephora.com'
        }
        
        try:
            api_response = requests.get(api_url, headers=headers)
            if api_response.status_code == 200:
                api_json = api_response.json()
                if api_json['currentSku']['skuId'] == skuId:
                    if api_json['currentSku']['actionFlags']['isAddToBasket'] == True:
                        item['product_status'] = '01'
                    else:
                        item['product_status'] = '00'
                else:
                    for i in api_json['regularChildSkus']:
                        if i['skuId'] == skuId:
                            if i['actionFlags']['isAddToBasket'] == True:
                                item['product_status'] = '01'
                            else:
                                item['product_status'] = '00'
        except Exception as e:
            print('error-----' + str(e))
        
        yield item
