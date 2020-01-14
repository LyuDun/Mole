from ext import db, Redis
from scrapy.cmdline import execute
from threading import Timer
cursor = db.cursor()

def manage_url():
    sql = """SELECT product_url FROM mole_product WHERE product_status = '00' """
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            url = row[0]
            Redis.lpush('sephora:start_urls', url)
    except Exception as e:
        print(e)
    finally:
        print('1')


class Time_task(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


if __name__ == '__main__':
    t = Time_task(10, manage_url)
    t.start()
    execute(['scrapy', 'crawl', 'sephora'])
