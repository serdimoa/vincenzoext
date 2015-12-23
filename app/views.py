# coding=utf-8
from __future__ import unicode_literals
import os
import ast
import json
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, make_response, Response
from flask.ext.login import login_user, logout_user, current_user, login_required
from sqlalchemy import sql, select
from werkzeug.utils import secure_filename
from app import app, db, lm, oid
from forms import LoginForm, CategoryForm, ItemForm
from models import User, Category, Items

basedir = os.path.abspath(os.path.dirname(__file__))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


# @app.route('/')
# @app.route('/index')
# @login_required
# def index():
#     user = g.user
#     posts = [
#         {
#             'author': { 'nickname': 'John' },
#             'body': 'Beautiful day in Portland!'
#         },
#         {
#             'author': { 'nickname': 'Susan' },
#             'body': 'The Avengers movie was so cool!'
#         }
#     ]
#     return render_template('index.html',
#         title = 'Home',
#         user = user,
#         posts = posts)
#

@app.route('/')
def index():
    select_category = Category.query.all()
    all_items = db.session.query(Items, Category).join(Category, Items.category_id == Category.id).all()
    return render_template("page.html", type=select_category, items=all_items, title="Vincenzo")


@app.route('/panel/category', methods=['GET', 'POST'])
def get_category():
    """
    Берем все категории или добавляем новую
    :rtype : json
    """
    select_category = Category.query.all()
    return render_template("category.html", category=select_category)


@app.route('/get_order', methods=['GET', 'POST'])
def get_order():
    order_detail = request.data
    order_convert = ast.literal_eval(order_detail)
    order_convert = map(int, order_convert)
    keys = ['id', 'item_name', 'item_component', 'price', 'weight']

    orders = db.session.execute(
        select(
            [Items.id, Items.item_name, Items.item_component, Items.price, Items.weight],
            Items.id.in_(order_convert)
            )
        ).fetchall()
    response_order = [dict(zip(keys, row)) for row in orders]

    return jsonify(response=response_order)


@app.route('/panel/category/category_add', methods=['GET', 'POST'])
def category_add():
    form = CategoryForm()
    if form.validate_on_submit():
        category_data = Category(category_name=form.category_name.data,
                                 alias=form.alias.data)
        db.session.add(category_data)
        db.session.commit()
        flash(u'Категория добавлена',"success")
        return redirect(url_for('get_category'))
    return render_template('category_add.html', form=form)


@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    """
    Удаляем категорию
    :rtype : redirect to category page
    """
    category = Category.query.get(category_id)
    Category.query.filter_by(id=category_id).delete()
    db.session.commit()
    flash("Удалена категория - " + category.category_name,"success")

    return redirect(url_for("get_category"))


@app.route('/update_category/<int:category_id>', methods=['GET', 'POST'])
def update_category(category_id):
    """
    Переименовуем категорию
    :rtype : flash
    """
    form = CategoryForm(obj=Category.query.filter_by(id=category_id).first())
    if form.validate_on_submit():
        category = Category.query.get(category_id)
        category.category_name = form.category_name.data
        category.alias = form.category_name.data
        db.session.commit()
        flash(u"Категория переименована на " + category.category_name, "info")
        return redirect(url_for("get_category"))

    return render_template("category_edit.html", form=form)


@app.route('/order', methods=['GET', 'POST'])
def order():
    return render_template("order.html")


@app.route('/get_one_item/<int:item_id>', methods=['GET','POST'])
def get_one_item(item_id):
    select_item = Items.query.filter_by(id=item_id).first()
    return jsonify(result=dict(id=select_item.id,
                               name=select_item.item_name,
                               imgs=select_item.img,
                               components=select_item.item_component,
                               weight=select_item.weight,
                               price=select_item.price
                               )
                   )


@app.route('/aboutus',methods=['GET','POST'])
def about_us():
    return render_template("aboutus.html", title="О нас")


@app.route('/panel/item_add',  methods=['GET', 'POST'])
def item_add():
    form = ItemForm()
    form.category_id.choices = [(c.id, c.category_name) for c in Category.query.all()]
    if request.method == 'POST':
        filename = secure_filename(form.img.data.filename)
        item_data = Items(
            item_name=form.item_name.data,
            item_component=form.item_component.data,
            category_id=form.category_id.data,
            weight=form.weight.data,
            price=form.price.data,
            img=form.item_name.data+filename

        )
        db.session.add(item_data)
        db.session.commit()
        form.img.data.save(basedir + "/static/upload/" + form.item_name.data + filename)
        flash("Добавлен новый товар", "success")
        return redirect(url_for("items"))

    return render_template('items_add.html', form=form)


@app.route('/panel/item_edit/<int:item_id>',  methods=['GET', 'POST'])
def item_edit(item_id):
    select_item = Items.query.filter_by(id=item_id).first()
    img = select_item.img
    form = ItemForm(obj=select_item)
    form.category_id.choices = [(c.id, c.category_name) for c in Category.query.all()]
    if request.method == 'POST':
        filename = secure_filename(form.img.data.filename)
        if filename:
            item = Items.query.get(item_id)
            item.item_name = form.item_name.data
            item.item_component = form.item_component.data
            item.category_id = form.category_id.data
            item.weight = form.weight.data
            item.price = form.price.data
            item.img = form.item_name.data+filename
            form.img.data.save(basedir + "/static/upload/" + form.item_name.data + filename)
            db.session.commit()
        else:
            item = Items.query.get(item_id)
            item.item_name = form.item_name.data
            item.item_component = form.item_component.data
            item.category_id = form.category_id.data
            item.weight = form.weight.data
            item.price = form.price.data
            item.img = img
            db.session.commit()

        flash(u"Изменено", "info")
        return redirect(url_for("items"))

    return render_template('items_edit.html', form=form, img=img)


@app.route('/panel/item_delete/<int:item_id>',  methods=['GET', 'POST'])
def item_delete(item_id):
    item = Items.query.get(item_id)
    Items.query.filter_by(id=item_id).delete()
    db.session.commit()
    flash("Удален - " + item.item_name, "success")
    return redirect(url_for("items"))


@app.route('/panel/items',  methods=['GET', 'POST'])
def items():
    all_items = db.session.query(Items, Category).join(Category, Items.category_id == Category.id).all()
    return render_template("items.html", items=all_items)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(emai=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(username=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
