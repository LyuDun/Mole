#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Email,EqualTo


class Mole_Product_Form(FlaskForm):
    product_url = StringField('网址', validators=[DataRequired(), URL(message=u'网址格式不正确'), Length(1, 512)])
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    phone_number = StringField('手机号', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    phone_number = StringField('手机号', validators=[DataRequired(), Length(1, 24)])
    email = StringField(label=u'邮箱地址',validators=[DataRequired(), Length(1,64), Email()])
    username = StringField(label=u'用户名',validators=[DataRequired(), Length(1,64)])
    password = PasswordField(label=u'密码',validators=[DataRequired(), EqualTo('password2', message=u'密码必须相同')])
    password2 = PasswordField(label=u'确认密码',validators=[DataRequired()])
    submit = SubmitField(label=u'马上注册')