import pymysql
from redis import StrictRedis
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

Redis = StrictRedis(host='localhost', port=6379, db=0,
                    decode_responses=True, password='1a2b3cmm2507')
db = pymysql.connect("localhost", "root", "1a2b3c", "mole")