# coding=utf-8
from __future__ import unicode_literals
import random
import string
import urllib
import urllib2
import simplejson as simplejson
from jinja2.filters import environmentfilter
import os
import ast
import json
import datetime
from time import gmtime, strftime, mktime
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, make_response, Response
from flask.ext.login import login_user, logout_user, current_user, login_required
from sqlalchemy import sql, select
from sqlalchemy_utils.types.locale import babel
from werkzeug.utils import secure_filename
from app import app, db, lm, oid
from forms import LoginForm, CategoryForm, ItemForm, RegistrationForm, UserEdit, SaleAddForm, ChangeUserPassword, \
    AuchForm, SaleOnTimeForm, OrdernoAuchForForDeliveryInCafe, OrdernoAuchForDeliveryInHome, \
    OrdernoAuchForForDeliveryMySelf
from models import User, Category, Items, Like, AnonymousUser, Sale, Adress, SaleoOnTime
import mandrill

lm.anonymous_user = AnonymousUser

basedir = os.path.abspath(os.path.dirname(__file__))


@app.template_filter()
def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq


app.jinja_env.filters['shuffle'] = filter_shuffle


@app.template_filter()
def format_datetime(value, format='medium'):
    if format == 'full':
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format = "EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)


app.jinja_env.filters['datetime'] = format_datetime


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None


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
    select_sale = Sale.query.all()
    delivery = request.cookies.get('delivery')
    if delivery == "deliveryincafe":
        global_sale = 0
    elif delivery == "deliverymyself":
        global_sale = 10
    elif delivery == "deliveryinhome":
        global_sale = 0
    else:
        global_sale = 0
    if current_user.id is None:
        select_category = Category.query.all()
        all_items = db.session.query(Items, Category).join(Category, Items.category_id == Category.id).all()
        return render_template("page.html", type=select_category, global_sale=global_sale, sales=select_sale,
                               delivery=delivery, items=all_items,
                               title="Vincenzo")
    else:
        select_category = Category.query.all()
        all_items = db.session.query(Items, Category).join(Category, Items.category_id == Category.id).all()
        likes = Like.query.filter_by(user_id=current_user.id).all()
        liked = []
        for likes in likes:
            liked.append(likes.items_id)

        return render_template("page.html", type=select_category, global_sale=global_sale, sales=select_sale,
                               items=all_items, likes=liked,
                               title="Vincenzo", delivery=delivery)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if current_user.is_authenticated:
        form = UserEdit(obj=User.query.filter_by(id=current_user.id).first(), prefix="form")
        form_password = ChangeUserPassword(prefix="form_password")
        if form_password.validate_on_submit() and form_password.is_submitted():
            item = User.query.get(current_user.id)
            if item.password == form_password.old_password.data:
                item.password = form_password.new_password.data
                db.session.commit()
                flash(u'Изменено', 'errors')
                return redirect(url_for("settings"))
            else:
                flash(u'Неправильный старый пароль', 'errors')
                return redirect(url_for("settings"))

        if form.validate_on_submit() and form.is_submitted():
            item = User.query.get(current_user.id)
            item.username = form.username.data
            item.phone = form.phone.data
            db.session.commit()
            flash(u'Изменено', 'errors')
            return redirect(url_for("settings"))

        return render_template("settings.html", form=form, form_password=form_password)
    else:
        return redirect(url_for("index"))


@app.route('/address', methods=['GET', 'POST'])
def address():
    if current_user.is_authenticated:
        if request.method == "POST":
            user_address = Adress.query.filter_by(user_id=current_user.id).first()
            if user_address is None:
                address_data = Adress(user_id=current_user.id, address=request.values.get('addresses'))
                db.session.add(address_data)
                db.session.commit()
                return jsonify(result="ok, is None")
            else:
                db.session.query(Adress).filter(Adress.user_id == current_user.id).update(
                    {'address': request.values.get('addresses')})
                db.session.commit()
                return jsonify(result="ok")

        elif request.method == 'GET':
            user_address = Adress.query.filter_by(user_id=current_user.id).all()
            addr = user_address[0].address
            return jsonify(result=addr)

        else:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


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
    get_order_order = request.cookies.get("cart")

    orders = simplejson.loads(get_order_order)
    orderis = ast.literal_eval(orders)
    return orders


@app.route('/panel/sale_time_add', methods=['GET', 'POST'])
def sale_time_add():
    form = SaleOnTimeForm()
    if form.validate_on_submit():
        sale_data = SaleoOnTime(sale_name=form.sale_name.data, down_sale=form.down_sale.data,
                                date_sale_on=str(form.date_sale_on.data), time_start=form.time_start.data,
                                time_end=form.time_end.data)
        db.session.add(sale_data)
        db.session.commit()
        flash("Добавлена новая акция", "success")
        return redirect(url_for('sale_time'))
    return render_template('sales_with_time.html', form=form, btn=u"Добавить")


@app.route('/get_sales', methods=['GET'])
def get_sales():
    keys = ['id', 'sale_name', 'down_sale', 'date_sale_on', 'time_start', 'time_end']
    orders = SaleoOnTime.query.all()
    response_order = list()
    # response_order = [dict(zip(keys, row)) for row in orders]
    for row in orders:
        if row.time_start < datetime.datetime.now() < row.time_end:
            response_order.append(row.id)

    return response_order


@app.route('/panel/sale_time_edit/<int:sale_id>', methods=['GET', 'POST'])
def sale_time_edit(sale_id):
    select_item = SaleoOnTime.query.filter_by(id=sale_id).first()
    form = SaleOnTimeForm(obj=select_item)
    if form.validate_on_submit():
        sale_data = SaleoOnTime(sale_name=form.sale_name.data, down_sale=form.down_sale.data,
                                date_sale_on=str(form.date_sale_on.data), time_start=form.time_start.data,
                                time_end=form.time_end.data)
        db.session.add(sale_data)
        db.session.commit()
        flash("Добавлена новая акция", "success")
        return redirect(url_for('sale'))
    return render_template('sales_with_time.html', form=form, btn=u"Изменить")


@app.route('/panel/sale/add', methods=["GET", "POST"])
def sale_add():
    form = SaleAddForm()
    if form.validate_on_submit():
        filename = secure_filename(form.img.data.filename)
        if filename:
            sale_data = Sale(sale_name=form.sale_name.data,
                             price_if_have=form.price_if_have.data,
                             about_sale=form.about_sale.data,
                             show_url=form.show_url.data,
                             end_sale=form.end_sale.data,
                             to_slider=form.to_slider.data,
                             img=form.sale_name.data + filename)
            db.session.add(sale_data)
            db.session.commit()
            form.img.data.save(basedir + "/static/upload/" + form.sale_name.data + filename)
            flash("Добавлена новая акция", "success")
            return redirect(url_for('sale'))
        else:
            sale_data = Sale(sale_name=form.sale_name.data,
                             price_if_have=form.price_if_have.data,
                             about_sale=form.about_sale.data,
                             show_url=form.show_url.data,
                             to_slider=form.to_slider.data
                             )
            db.session.add(sale_data)
            db.session.commit()
            flash("Добавлена новая акция", "success")
            return redirect(url_for('sale'))
    return render_template('sales_add.html', form=form)


@app.route('/panel/sales_time', methods=["GET"])
def sale_time():
    all_sales = db.session.query(SaleoOnTime).all()
    return render_template("sales_time.html", items=all_sales)


@app.route('/panel/sales', methods=["GET"])
def sale():
    all_sales = db.session.query(Sale).all()
    return render_template("sales.html", items=all_sales)


@app.route('/panel/sale_edit/<int:sale_id>', methods=['GET', 'POST'])
def sale_edit(sale_id):
    select_item = Sale.query.filter_by(id=sale_id).first()
    img = select_item.img
    form = SaleAddForm(obj=select_item)
    if form.validate_on_submit():
        filename = secure_filename(form.img.data.filename)
        if filename:
            item = Sale.query.get(sale_id)
            item.sale_name = form.sale_name.data
            item.price_if_have = form.price_if_have.data
            item.about_sale = form.about_sale.data
            item.show_url = form.show_url.data
            item.end_sale = form.end_sale.data
            item.to_slider = form.to_slider.data
            item.img = form.sale_name.data + filename
            form.img.data.save(basedir + "/static/upload/" + form.sale_name.data + filename)
            db.session.commit()
        else:
            item = Sale.query.get(sale_id)
            item.sale_name = form.sale_name.data
            item.to_slider = form.to_slider.data
            item.end_sale = form.end_sale.data
            item.price_if_have = form.price_if_have.data
            item.about_sale = form.about_sale.data
            item.show_url = form.show_url.data
            item.img = img
            db.session.commit()

        flash(u"Изменено", "info")
        return redirect(url_for("sale"))

    return render_template('sale_edit.html', form=form, img=img)


@app.route('/panel/sales_delete/<int:item_id>', methods=['GET', 'POST'])
def sale_delete(item_id):
    item = Sale.query.get(item_id)
    Sale.query.filter_by(id=item_id).delete()
    db.session.commit()
    flash("Удален - " + item.sale_name, "success")
    return redirect(url_for("sale"))


@app.route('/panel/category/category_add', methods=['GET', 'POST'])
def category_add():
    form = CategoryForm()
    if form.validate_on_submit():
        category_data = Category(category_name=form.category_name.data,
                                 alias=form.alias.data, sous=form.sous.data, cafe=form.cafe.data)
        db.session.add(category_data)
        db.session.commit()
        flash(u'Категория добавлена', "success")
        return redirect(url_for('get_category'))
    return render_template('category_add.html', form=form)


@app.route('/like_add', methods=['GET', 'POST'])
def like_add():
    if current_user is None:
        return jsonify(result=0)
    else:
        items_id = request.args.get('like')
        have_like = Like.query.filter_by(user_id=current_user.id, items_id=items_id).first()
        if have_like is None:
            like = Like(user_id=current_user.id, items_id=items_id)
            db.session.add(like)
            db.session.commit()
            return jsonify(result="adfavorited")
        else:
            Like.query.filter_by(user_id=current_user.id, items_id=items_id).delete()
            db.session.commit()
            return jsonify(result="delete")


@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    """
    Удаляем категорию
    :rtype : redirect to category page
    """
    category = Category.query.get(category_id)
    Category.query.filter_by(id=category_id).delete()
    db.session.commit()
    flash("Удалена категория - " + category.category_name, "success")

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
        category.alias = form.alias.data
        category.sous = form.sous.data
        category.cafe = form.cafe.data
        db.session.commit()
        flash(u"Категория " + category.category_name + u" Изменена", "info")
        return redirect(url_for("get_category"))

    return render_template("category_edit.html", form=form)


@app.route('/order', methods=['GET', 'POST'])
def order():
    form1 = OrdernoAuchForForDeliveryInCafe()
    form2 = OrdernoAuchForForDeliveryMySelf()
    form3 = OrdernoAuchForDeliveryInHome()
    delivery = request.cookies.get('delivery')
    carts = request.cookies.get("cart")
    if delivery == "deliveryincafe":
        global_sale = 0
        form = form1
    elif delivery == "deliverymyself":
        form = form2
        global_sale = 10
    elif delivery == "deliveryinhome":
        global_sale = 0
        form = form3
    else:
        form = form3
        global_sale = 0
    if form.validate_on_submit():
        if form.hidden_type.data == "deliveryinhome":
            flash(u"Заказ оформлен deliveryinhome", 'success')
            return redirect(url_for('order'))
        if form.hidden_type.data == "deliveryincafe":
            flash(u"Заказ оформлен deliveryincafe", 'success')
            return redirect(url_for('order'))
        if form.hidden_type.data == "deliverymyself":
            flash(form.delivery_time.data, 'success')
            try:
                mandrill_client = mandrill.Mandrill('wv39DASQNMJbfCratNJa2w')
                message = {
                    'auto_html': None,
                    'auto_text': None,
                    'from_email': 'sir.vincenzo.office@gmail.com',
                    'from_name': 'Sir Vincenzo ',
                    'headers': {'Reply-To': 'sir.vincenzo.office@gmail.com'},
                    'html': '<div>Ваш Заказ с сайта: ' +carts.decode('utf8')  + '</div>',
                    'subject': 'Ваш Заказ с сайта Sir Vincenzo ',
                    'to': [{'email': "serdimoa@gmail.com",
                            'name': "serdimoa",
                            'type': 'to'}]
                    }

                result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
                return jsonify(result=result[0]['status'])

            except mandrill.Error, e:  # Mandrill errors are thrown as exceptions
               return jsonify(result=2)
    else:
        if current_user.id is None:
            settings_it = [str("delete_buy_button"), str(delivery)]
            return render_template("order.html",  form=form, title="Vincenzo",
                                   settings_order=settings_it, global_sale=global_sale)
        else:
            user_address = Adress.query.filter_by(user_id=current_user.id).first()
            addreses = eval(user_address.address)
            return render_template("order.html", title="Vincenzo", addreses=addreses, global_sale=global_sale)


@app.route('/deliveryinhome', methods=["POST","GET"])
def post_deliveryinhome():
    form = OrdernoAuchForDeliveryInHome()
    if form.validate():
        flash(u"Заказ оформлен deliveryinhome", 'success')
        return redirect(url_for('order'))
    return redirect(url_for('order'))


@app.route('/get_one_item/<int:item_id>', methods=['GET', 'POST'])
def get_one_item(item_id):
    select_item = db.session.query(Items, Category).filter_by(id=item_id). \
        join(Category, Items.category_id == Category.id).first()
    # select_item = Items.query.
    return jsonify(result=dict(item_id=select_item[0].id,
                               name=select_item[0].item_name,
                               imgs=select_item[0].img,
                               components=select_item[0].item_component,
                               weight=select_item[0].weight,
                               price=select_item[0].price,
                               cafe_only=select_item[0].cafe_only,
                               category=select_item[1].category_name,
                               sous=select_item[1].sous
                               )

                   )


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    select_sales = Sale.query.all()
    delivery = request.cookies.get('delivery')
    if delivery == "deliveryincafe":
        global_sale = 0
    elif delivery == "deliverymyself":
        global_sale = 10
    elif delivery == "deliveryinhome":
        global_sale = 0
    else:
        global_sale = 0
    return render_template('sale.html', sales=select_sales, global_sale=global_sale)


@app.route('/one_sale/<int:sale_id>', methods=['GET', 'POST'])
def one_sale(sale_id):
    delivery = request.cookies.get('delivery')
    if delivery == "deliveryincafe":
        global_sale = 0
    elif delivery == "deliverymyself":
        global_sale = 10
    elif delivery == "deliveryinhome":
        global_sale = 0
    else:
        global_sale = 0
    one_sales = db.session.query(Sale).filter_by(id=sale_id).first()
    return render_template('one_sale.html', sale=one_sales, global_sale=global_sale)


@app.route('/aboutus', methods=['GET', 'POST'])
def about_us():
    delivery = request.cookies.get('delivery')
    if delivery == "deliveryincafe":
        global_sale = 0
    elif delivery == "deliverymyself":
        global_sale = 10
    elif delivery == "deliveryinhome":
        global_sale = 0
    else:
        global_sale = 0
    return render_template("aboutus.html", title="О нас", global_sale=global_sale)


@app.route('/panel/item_add', methods=['GET', 'POST'])
def item_add():
    form = ItemForm()
    form.category_id.choices = [(c.id, c.category_name) for c in Category.query.all()]
    if request.method == 'POST':
        filename = secure_filename(form.img.data.filename)
        thumbnail = secure_filename(form.thumbnail.data.filename)
        item_data = Items(
            item_name=form.item_name.data,
            item_component=form.item_component.data,
            category_id=form.category_id.data,
            weight=form.weight.data,
            price=form.price.data,
            cafe_only=form.cafe_only.data,
            img=form.item_name.data + filename,
            thumbnail=form.item_name.data + "thumbnail" + thumbnail

        )
        db.session.add(item_data)
        db.session.commit()
        form.img.data.save(basedir + "/static/upload/" + form.item_name.data + filename)
        form.thumbnail.data.save(basedir + "/static/upload/" + form.item_name.data + "thumbnail" + thumbnail)
        flash("Добавлен новый товар", "success")
        return redirect(url_for("items"))

    return render_template('items_add.html', form=form)


@app.route('/panel/item_edit/<int:item_id>', methods=['GET', 'POST'])
def item_edit(item_id):
    select_item = Items.query.filter_by(id=item_id).first()
    img = select_item.img
    thumb = select_item.thumbnail
    form = ItemForm(obj=select_item)
    form.category_id.choices = [(c.id, c.category_name) for c in Category.query.all()]
    if request.method == 'POST':
        filename = secure_filename(form.img.data.filename)
        thumbnail = secure_filename(form.thumbnail.data.filename)
        if filename and thumbnail:  # Есть картика и миниатюра
            item = Items.query.get(item_id)
            item.item_name = form.item_name.data
            item.item_component = form.item_component.data
            item.category_id = form.category_id.data
            item.weight = form.weight.data
            item.price = form.price.data
            item.cafe_only = form.cafe_only.data
            item.img = form.item_name.data + filename
            item.thumbnail = form.item_name.data + "thumbnail" + thumbnail
            form.img.data.save(basedir + "/static/upload/" + form.item_name.data + filename)
            form.thumbnail.data.save(basedir + "/static/upload/" + form.item_name.data + "thumbnail" + thumbnail)
            db.session.commit()

        elif filename and not thumbnail:  # Есть картика, но нет миниатюры
            item = Items.query.get(item_id)
            item.item_name = form.item_name.data
            item.item_component = form.item_component.data
            item.category_id = form.category_id.data
            item.weight = form.weight.data
            item.price = form.price.data
            item.cafe_only = form.cafe_only.data
            item.img = form.item_name.data + filename
            item.thumbnail = thumb
            form.img.data.save(basedir + "/static/upload/" + form.item_name.data + filename)
            db.session.commit()

        elif thumbnail and not filename:  # Есть миниатюра, но нет картинки
            item = Items.query.get(item_id)
            item.item_name = form.item_name.data
            item.item_component = form.item_component.data
            item.category_id = form.category_id.data
            item.weight = form.weight.data
            item.price = form.price.data
            item.cafe_only = form.cafe_only.data
            item.img = img
            form.thumbnail.data.save(basedir + "/static/upload/" + form.item_name.data + "thumbnail" + thumbnail)
            item.thumbnail = form.item_name.data + "thumbnail" + thumbnail
            db.session.commit()

        else:  # нет миниатюры и нет картинки
            item = Items.query.get(item_id)
            item.item_name = form.item_name.data
            item.item_component = form.item_component.data
            item.category_id = form.category_id.data
            item.weight = form.weight.data
            item.price = form.price.data
            item.cafe_only = form.cafe_only.data
            item.img = img
            item.thumbnail = thumb
            db.session.commit()

        flash(u"Изменено", "info")
        return redirect(url_for("items"))

    return render_template('items_edit.html', form=form, img=img)


@app.route('/panel/item_delete/<int:item_id>', methods=['GET', 'POST'])
def item_delete(item_id):
    item = Items.query.get(item_id)
    Items.query.filter_by(id=item_id).delete()
    db.session.commit()
    flash("Удален - " + item.item_name, "success")
    return redirect(url_for("items"))


@app.route('/panel/items', methods=['GET', 'POST'])
def items():
    all_items = db.session.query(Items, Category).join(Category, Items.category_id == Category.id).all()
    return render_template("items.html", items=all_items)


#
# @oid.after_login
# def after_login(resp):
#     if resp.email is None or resp.email == "":
#         flash('Invalid login. Please try again.')
#         return redirect(url_for('login'))
#     user = User.query.filter_by(emai=resp.email).first()
#     if user is None:
#         nickname = resp.nickname
#         if nickname is None or nickname == "":
#             nickname = resp.email.split('@')[0]
#         user = User(username=nickname, email=resp.email)
#         db.session.add(user)
#         db.session.commit()
#     remember_me = False
#     if 'remember_me' in session:
#         remember_me = session['remember_me']
#         session.pop('remember_me', None)
#     login_user(user, remember=remember_me)
#     return redirect(request.args.get('next') or url_for('index'))
#


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/auch', methods=['GET', 'POST'])
def auch():
    username = request.args.get('login')
    password = request.args.get('password')
    registered_user = User.query.filter_by(phone=username, password=password).first()
    if registered_user is None:
        return jsonify(result=0)
    login_user(registered_user)
    return jsonify(result=1)


@app.route('/pwreset', methods=['GET', 'POST'])
def pwreset():
    login = request.args.get('login')
    is_user = User.query.filter_by(phone=login).first()
    if is_user is None:
        return jsonify(result=0)
    try:
        new_password = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
        mandrill_client = mandrill.Mandrill('wv39DASQNMJbfCratNJa2w')
        message = {
            'auto_html': None,
            'auto_text': None,
            'from_email': 'sir.vincenzo.office@gmail.com',
            'from_name': 'Востановление пароля Sir Vincenzo ',
            'headers': {'Reply-To': 'sir.vincenzo.office@gmail.com'},
            'html': '<p>Ваш новый пароль: ' + new_password + '</p>',
            'subject': 'Востановление пароля с сайта Sir Vincenzo ',
            'to': [{'email': is_user.email,
                    'name': is_user.username,
                    'type': 'to'}]
        }
        user = User.query.get(is_user.id)
        user.password = new_password
        db.session.commit()
        result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
        return jsonify(result=result[0]['status'])

    except mandrill.Error, e:  # Mandrill errors are thrown as exceptions
        return jsonify(result=2)

        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    delivery = request.cookies.get('delivery')
    if delivery == "deliveryincafe":
        global_sale = 0
    elif delivery == "deliverymyself":
        global_sale = 10
    elif delivery == "deliveryinhome":
        global_sale = 0
    else:
        global_sale = 0
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    phone=form.phone.data,
                    authenticated=True)
        db.session.add(user)
        db.session.commit()
        registered_user = User.query.filter_by(phone=form.phone.data, global_sale=global_sale,
                                               password=form.password.data).first()
        if registered_user is None:
            return redirect(url_for('index'))
        login_user(registered_user)
        return redirect(url_for('index'))
    return render_template("registration.html", form=form)


@app.route('/site_auch', methods=['GET', 'POST'])
def site_auch():
    form = RegistrationForm(prefix="form")
    form_auch = AuchForm(prefix="form_auch")
    if form.validate_on_submit() and form.is_submitted():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    phone=form.phone.data,
                    authenticated=True)
        db.session.add(user)
        db.session.commit()
        registered_user = User.query.filter_by(phone=form.phone.data, password=form.password.data).first()
        if registered_user is None:
            return redirect(url_for('index'))
        login_user(registered_user)
        return redirect(url_for('index'))

    if form_auch.validate_on_submit() and form_auch.is_submitted():
        username = form_auch.login.data
        password = form_auch.password.data
        registered_user = User.query.filter_by(phone=username, password=password).first()
        if registered_user is None:
            flash(u'Логин либо пароль не верны', 'errors')
            return redirect("site_auch")
        login_user(registered_user)
        return redirect(url_for('index'))
    return render_template("siteauch.html", form=form, form_auch=form_auch)
