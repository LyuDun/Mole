from scrapy_mole import Redis
from scrapy_mole import get_urls
import scrapy
from scrapy_mole.items import ScrapyMoleItem


class Sephora_scrapy(scrapy.Spider):
    name = 'sephora'
    allowed_domains = ["sephora.com"]
    CURRENT_PAGE = 1

    def parse(self, response):
        for url in get_urls(index=1):
            yield scrapy.Request(url, callback=self.parse_url(url))

    def parse_url(self, response, url):
        item = ScrapyMoleItem()
        try:
            item['product_url'] = url
            str1 = response.selector.xpath(
                '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/h1/a/span/text()')
            str2 = response.selector.xpath(
                '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/h1/span/text()')
            item['product_name'] = str1 + str2
            item['product_img'] = response.selector.xpath(
                '//*[@id="tabItem_6wt_1_0"]/div/div/div/img')

            variations = response.selector.xpath(
                '/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/span/text()').extract()
            tmp = ''
            for variation in variations:
                tmp = tmp + variation
            item['product_variation'] = tmp
            button = response.selector.xpath('/html/body/div[2]/div[5]/main/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[7]/button').extract()[
                0].replace('<', '').replace('>', '').replace('/', '')
            '''
            button data-at="selected_swatch" aria-selected="false" aria-live="polite" 
            aria-atomic="true" aria-describedby="colorSwatch" 
            aria-label="Out of stock: 26 All Washed  Up (matte finish)" class="css-1j1jwa4"div aria-hidden="true"img src="https:www.sephora.comproductimagesskus1934959+sw.jpg" alt="SEPHORA COLLECTION - #LIPSTORIES   26 All Washed  Up (matte finish) 0.14 oz 4 g" 
            class="css-qx1w30 " data-comp="Image Box"divdiv aria-hidden="true" class="css-12wq9x9"divbutton
            '''
            search_obj = re.search('Out of stock', button)
            if search_obj:
                item['product_status'] = 'Y'
                print('----------------------')
            else:
                item["product_status"] = 'N'
            yield item
        except Exception as e:
            print('err-----' + str(e))
