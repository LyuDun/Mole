from ext import DB , Redis
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from contextlib import contextmanager

sender = '1778116108@qq.com'
subject = '您在鼹鼠监控的商品现已有货'
smtpserver = 'smtp.qq.com'
#username = 'cqcqhelloworld@gmail.com'
#password = '1a2b3cmm2507@@CQ'
username = '1778116108@qq.com'
password = 'ryjcafrgjhyngaeg'


scheduler = BlockingScheduler()

def manage_url():
    sql = "SELECT distinct product_url FROM mole_product WHERE product_status = '00' "
    with DB() as db:
        db.execute(sql)
        results = db.fetchall()
        #print('长度'+ str(len(results)))
        if len(results) == 0:
            return
        else:
            for row in results:
                url = row['product_url']
                Redis.lpush('sephora:start_urls', url)
def send_email():
    sql = "SELECT mp.phone_number as phone_number, product_url, product_name, product_variation, update_time, email FROM mole_product mp, mole_user mu WHERE mp.product_status = '01' AND mu.email_notice = 'Y' AND mp.phone_number = mu.phone_number"
    with DB() as db:
        db.execute(sql)
        results = db.fetchall()
        #print('长度'+ str(len(results)))
        if len(results) == 0:
            return
        else:
            with logined(username, password) as smtp_serv:
                for row in results:
                    html_str ="""<p>Hi! {}<br>你在<a href="http://www.cqcqhelloworld.top/">鼹鼠</a>监控的商品{} {},现已({})有货<br>点击<a href="{}">链接</a>，跳转到网站，开始购物吧</p>""".format(row['phone_number'], row['product_name'], row['product_variation'], row['update_time'], row['product_url'])
                    msg=MIMEText(html_str,'html','utf-8')
                    msg['From'] = sender
                    msg['To'] = row['email']
                    msg['Subject'] = Header("鼹鼠提醒", 'utf-8')
                    try:
                        smtp_serv.send_message(msg)
                        #smtp.sendmail(sender, row['email'], msg.as_string())
                        sql2 = "UPDATE mole_product SET product_status = '10' WHERE phone_number ='{}' AND product_url = '{}'".format(row['phone_number'], row['product_url'])
                        db.execute(sql2)
                        print(sql2)
                    finally:
                        pass
@contextmanager
def logined(sender, password, smtp_host='smtp.qq.com', smtp_port=587):
    smtp_serv = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
    try: # make smtp server and login
        smtp_serv.ehlo_or_helo_if_needed()
        smtp_serv.starttls()
        smtp_serv.ehlo()
        smtp_serv.login(sender, password)
        yield smtp_serv
    finally:
        pass

def dojob():
    scheduler.add_job(manage_url, 'interval', seconds=8, id='job1')
    scheduler.add_job(send_email, 'interval', seconds=15, id='job2')
    scheduler.start()

if __name__ == '__main__':
    dojob()
