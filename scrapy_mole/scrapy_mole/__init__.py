from redis import StrictRedis
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

Redis = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def get_urls(index=1):
    '''
    index:
        1: sephora
    '''
    if 1 == index:
        pattern = 'sephora*'
    urls = redis.keys(pattern)
    return urls
