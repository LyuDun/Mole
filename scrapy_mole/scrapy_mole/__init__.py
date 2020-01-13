import pymysql
from redis import StrictRedis
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

Redis = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, password='1a2b3cmm2507')
db = pymysql.connect("localhost", "root", "1a2b3c", "mole")




def get_urls(index=1):
    '''
    index:
        1: sephora
    '''
    url_list = []
    if 1 == index:
        pattern = 'sephora*'
    urls = redis.keys(pattern)
    for url in urls:
        url_list.append(redis.hmget(url, 'product_url'))
    logging.warning('url_list--:'+ str(url_list))
    return url_list
