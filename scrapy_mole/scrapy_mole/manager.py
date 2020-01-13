from scrapy_mole import Redis, db
cursor = db.cursor()
# 从数据库表mole_product 取状态为00的记录， 写入redis的list


def manage_url():

    sql = """SELECT product_url FROM mole_product WHERE product_status == '00' """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            url = row[0]
            Redis.lpush('sephora:start_urls', url)
