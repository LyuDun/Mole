#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, URL, Email, EqualTo, InputRequired


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

class UserForm(FlaskForm):
    new_email = StringField(label=u'新邮箱',validators=[Length(1,64), Email()])
    submit_newemail = SubmitField(label=u'更换邮箱')
    
    password = PasswordField(label=u'密码',validators=[EqualTo('password2', message=u'密码必须相同')])
    password2 = PasswordField(label=u'确认密码')
    update_password = SubmitField(label=u'更新密码')

    email_notice = SelectField('是否邮件通知', choices=[(1,"是"),(2,"否")], validators=[InputRequired], default=1, coerce=int)
    update_email_notice = SubmitField(label=u'更新邮件通知')
