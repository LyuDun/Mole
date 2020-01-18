#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user

from forms import Mole_Product_Form, LoginForm, RegisterForm
from ext import  db,login_manager
from flask_sqlalchemy import SQLAlchemy
from models import Mole_Product, Mole_User
from flask_cors import CORS

SECRET_KEY = 'This is my key'

app = Flask(__name__)
bootstrap = Bootstrap(app)
CORS(app)

app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:1a2b3c@localhost:3306/mole"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

db.init_app(app)
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = u'对不起，您还没有登录'


@app.route('/', methods=['GET', 'POST'])
@login_required
def show_url_list():
    form = Mole_Product_Form()
    if request.method == 'GET':
        mole_product = Mole_Product.query.filter_by(phone_number=current_user.phone_number)
        return render_template('index.html', mole_product=mole_product, form=form)
    else:
        if form.validate_on_submit():
            mole_product = Mole_Product(
                current_user.phone_number, form.product_url.data)
            db.session.add(mole_product)
            db.session.commit()
            flash('You have added a new URL to monitor')
        else:
            flash(form.errors)
        return redirect(url_for('show_url_list'))


@app.route('/delete/<int:id>')
@login_required
def delete_url_list(id):
    mole_product = Mole_Product.query.filter_by(id=id, phone_number=current_user.phone_number).first()
    db.session.delete(mole_product)
    db.session.commit()
    flash('You have delete a url')
    return redirect(url_for('show_url_list'))


@app.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change_url_list(id):
    if request.method == 'GET':
        mole_product = Mole_Product.query.filter_by(phone_number=current_user.phone_number).first()
        form = Mole_Product_Form()
        form.product_url.data = mole_product.product_url
        return render_template('modify.html', form=form)
    else:
        form = Mole_Product_Form()
        if form.validate_on_submit():
            mole_product = Mole_Product.query.filter_by(
                id=id).first_or_404()
            mole_product.product_url = form.product_url.data
            db.session.commit()
            flash('You have modify a url')
        else:
            flash(form.errors)
        return redirect(url_for('show_url_list'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            phone_number=request.form.get('phone_number')
            password=request.form.get('password')
            user = Mole_User.query.filter_by(phone_number=phone_number, password=password).first()
            if user:
                login_user(user)
                flash('you have logged in!')
                return redirect(url_for('show_url_list'))
            else:
                flash('Invalid username or password')
        except Exception as e:
            print(e)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logout!')
    return redirect(url_for('login'))


@app.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Mole_User(phone_number=request.form.get('phone_number'), username=request.form.get('username'), password=request.form.get('password'), email=request.form.get('email'))  # 新添加一个用户到数据库中
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(u'注册成功')
            return redirect(url_for('show_url_list'))
    else:
        return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return Mole_User.query.filter_by(id=int(user_id)).first()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)