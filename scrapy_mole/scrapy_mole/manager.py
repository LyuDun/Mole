from ext import db, Redis
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

if __name__ == '__main__':
    manage_url()