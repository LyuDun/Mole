from ext import DB , Redis
from apscheduler.schedulers.blocking import BlockingScheduler
scheduler = BlockingScheduler()

def manage_url():
    sql = "SELECT product_url FROM mole_product WHERE product_status = '00' "
    with DB() as db:
        db.execute(sql)
        results = db.fetchall()
        print('长度'+ str(len(results)))
        if len(results) == 0:
            return
        else:
            for row in results:
                url = row['product_url']
                Redis.lpush('sephora:start_urls', url)

def dojob():
    scheduler.add_job(manage_url, 'interval', seconds=8, id='job1')
    scheduler.start()

if __name__ == '__main__':
    dojob()
