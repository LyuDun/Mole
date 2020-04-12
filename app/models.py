#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from datetime import datetime
import pytz
from ext import db
from flask_login import UserMixin

tz = pytz.timezone('Asia/Shanghai')

class Mole_Product(db.Model):
    __tablename__ = 'mole_product'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(18))
    product_url = db.Column(db.String(512), nullable=False)
    product_name = db.Column(db.String(512))
    product_img = db.Column(db.String(512))
    product_variation = db.Column(db.String(128))
    product_status = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime)

    def __init__(self, phone_number, product_url):
        self.phone_number = phone_number
        self.product_url = product_url
        #self.product_name = product_name
        #self.product_variation = product_variation
        self.product_status = '00'
        mytime = datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        self.create_time = mytime 
        self.update_time = mytime


class Mole_User(UserMixin, db.Model):
    __tablename__ = "mole_user"
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(18))
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)
    wechat_id = db.Column(db.String(30))
    wechat_name = db.Column(db.String(60))
    email = db.Column(db.String(40))
    wechat_notice = db.Column(db.String(1), default='N')
    email_notice = db.Column(db.String(1), default='Y')

    def __init__(self, phone_number, username, password, email):
        self.phone_number = phone_number
        self.username = username
        self.password = password
        self.email = email
