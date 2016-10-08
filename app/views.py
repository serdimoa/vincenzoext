# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import random
import string
import urllib
import urllib2
import simplejson as simplejson
from jinja2.filters import environmentfilter
import os
import chardet
import ast
import json
import datetime
from time import gmtime, strftime, mktime
from flask import Markup, render_template, flash, redirect, session, url_for, request, g, jsonify, make_response, \
    Response
from flask.ext.login import login_user, logout_user, current_user, login_required
from sqlalchemy import sql, select
from sqlalchemy_utils.types.locale import babel
from werkzeug.utils import secure_filename
from app import app, db, lm, oid
from forms import LoginForm, CategoryForm, ItemForm, RegistrationForm, UserEdit, SaleAddForm, ChangeUserPassword, \
    AuchForm, SaleOnTimeForm, OrdernoAuchForForDeliveryInCafe, OrdernoAuchForDeliveryInHome, \
    OrdernoAuchForForDeliveryMySelf, TeaCategoryForm, TeaForm, OrderAuchForForDeliveryInCafe, \
    OrderAuchForForDeliveryMySelf, OrderAuchForDeliveryInHome, FormAddress, AdminLoginForm
from models import User, Category, Items, Like, AnonymousUser, Sale, Adress, SaleoOnTime, TeaCategory, Tea
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

lm.anonymous_user = AnonymousUser

basedir = os.path.abspath(os.path.dirname(__file__))

admin_login = "vincenzoadmin"
admin_password = "mGZ58n<3%m{y{iW"

fromaddr = "serdimoa@gmail.com"
toaddr = "sir.vincenzo.office@gmail.com"
mypass = "Ferateam1"


def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq


app.jinja_env.filters['shuffle'] = filter_shuffle


def firstorder():
    if current_user.first_order:
        return '<br><strong>Первый заказ</strong>'
    else:
        return ''


def selectdeliveretext(delselect):
    varies = {'500': u'По городу - от 500р.', '799': u'Пром.зона - от 800р.',
              '800': u'Старый Вартовск {район Энтузиастов} - от 800р.',
              '1000': u'Старый Вартовск {район "Горбатый"} - от 1000р.',
              '1200': u'Старый Вартовск {район "ЛПХ"и далее} - от 1200р.',
              '1500': u'Излучинск - от 1500р.'}
    tests = varies[delselect]
    return varies[delselect]


@app.route('/logoutadmin')
def logoutadmin():
    session.pop('logged_in', None)
    return redirect(url_for('adminlogin'))


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
    delivery = request.cookies.get('delivery')
    if delivery == "deliveryincafe":
        g.deliverymethod = u"В кафе"
        g.global_sale = 0
    elif delivery == "deliverymyself":
        g.deliverymethod = u"Самовывоз"
        g.global_sale = 10
    elif delivery == "deliveryinhome":
        g.deliverymethod = u"Доставка на дом"
        g.global_sale = 0
    else:
        g.deliverymethod = u"Доставка на дом"
        g.global_sale = 0

    g.delivery = delivery
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

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.admin.data == admin_login and form.password.data == admin_password:
            session['logged_in'] = True
            return redirect(url_for('items'))
        else:
            flash(u"Что-то не так", 'info')
            return redirect(url_for('adminlogin'))

    return render_template("admin_login.html", form=form)


@app.route('/')
def index():
    select_sale = Sale.query.all()
    delivery = request.cookies.get('delivery')
    if current_user.id is None:
        select_category = Category.query.all()
        all_items = db.session.query(Items, Category).join(Category, Items.category_id == Category.id).all()
        return render_template("page.html", type=select_category, sales=select_sale,
                               delivery=delivery, items=all_items,
                               title="Vincenzo")
    else:
        select_category = Category.query.all()
        all_items = db.session.query(Items, Category).join(Category, Items.category_id == Category.id).all()
        likes = Like.query.filter_by(user_id=current_user.id).all()
        liked = []
        for likes in likes:
            liked.append(likes.items_id)

        return render_template("page.html", type=select_category, sales=select_sale,
                               items=all_items, likes=liked,
                               title="Vincenzo", delivery=delivery)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if current_user.is_authenticated:
        form = UserEdit(obj=User.query.filter_by(id=current_user.id).first(), prefix="form")
        form_password = ChangeUserPassword(prefix="form_password")
        form_address = FormAddress(obj=Adress.query.filter_by(user_id=current_user.id).first(), prefix="form_address")
        item = User.query.get(current_user.id)

        if form_password.validate_on_submit():
            if form_password.is_submitted():
                if form_password.hidden_field.data == "ChangeUserPassword":
                    item = User.query.get(current_user.id)
                    if item.password == form_password.old_password.data:
                        item.password = form_password.new_password.data
                        db.session.commit()
                        flash(u'Изменено', 'errors')
                        return redirect(url_for("settings"))
                    else:
                        flash(u'Неправильный старый пароль', 'errors')
                        return redirect(url_for("settings"))

        if request.method == 'POST' and form.phone.data == item.phone and form.hidden_field.data == "UserEdit":
            db.session.query(Adress).filter(Adress.user_id == current_user.id).update(
                {'username': form.username.data})
            db.session.commit()
            flash(u'Изменено', 'errors')
            return redirect(url_for("settings"))
        if form.validate_on_submit():
            if form.is_submitted():
                if form.hidden_field.data == "UserEdit":
                    if form.phone.data != item.phone:
                        if User.query.filter_by(phone=form.phone.data).first() is not None:
                            flash(u'Такой телефон существует', 'errors')
                        else:
                            db.session.query(Adress).filter(Adress.user_id == current_user.id).update(
                                {'username': form.username.data,
                                 'phone': form.phone.data})
                            db.session.commit()
                            flash(u'Изменено', 'errors')
                        return redirect(url_for("settings"))

        if form_address.validate_on_submit():
            if form_address.is_submitted():
                if form_address.hidden_field.data == "FormAddress":
                    user_address = Adress.query.filter_by(user_id=current_user.id).first()
                    if user_address is None:
                        address_data = Adress(
                            user_id=current_user.id,
                            select_region=form_address.select_region.data,
                            street=form_address.street.data,
                            home=form_address.home.data,
                            home_corp=form_address.home_corp.data,
                            porch=form_address.porch.data,
                            domofon=form_address.domofon.data,
                            floor=form_address.floor.data,
                            kvartira=form_address.kvartira.data
                        )
                        db.session.add(address_data)
                        db.session.commit()
                    else:
                        db.session.query(Adress).filter(Adress.user_id == current_user.id).update(
                            {'select_region': form_address.select_region.data,
                             'street': form_address.street.data,
                             'home': form_address.home.data,
                             'home_corp': form_address.home_corp.data,
                             'porch': form_address.porch.data,
                             'domofon': form_address.domofon.data,
                             'floor': form_address.floor.data,
                             'kvartira': form_address.kvartira.data
                             })
                        db.session.commit()
                    flash(u'Изменено', 'errors')
                    return redirect(url_for("settings"))

        return render_template("settings.html", form_address=form_address, form=form, form_password=form_password)
    else:
        return redirect(url_for("index"))


@app.route('/panel/tea_category', methods=['GET', 'POST'])
def get_tea_category():
    """
    Берем все категории или добавляем новую
    :rtype : json
    """
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    select_category = TeaCategory.query.all()
    return render_template("teacategory.html", category=select_category)


@app.route('/panel/category', methods=['GET', 'POST'])
def get_category():
    """
    Берем все категории или добавляем новую
    :rtype : json
    """
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    select_category = Category.query.all()
    return render_template("category.html", category=select_category)


@app.route('/panel/sale_time_add', methods=['GET', 'POST'])
def sale_time_add():
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

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
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

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
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

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
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    all_sales = db.session.query(SaleoOnTime).all()
    return render_template("sales_time.html", items=all_sales)


@app.route('/panel/sales', methods=["GET"])
def sale():
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    all_sales = db.session.query(Sale).all()
    return render_template("sales.html", items=all_sales)


@app.route('/panel/sale_edit/<int:sale_id>', methods=['GET', 'POST'])
def sale_edit(sale_id):
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

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
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    item = Sale.query.get(item_id)
    Sale.query.filter_by(id=item_id).delete()
    db.session.commit()
    flash("Удален - " + item.sale_name, "success")
    return redirect(url_for("sale"))


@app.route('/panel/category/category_add', methods=['GET', 'POST'])
def category_add():
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    form = CategoryForm()
    if form.validate_on_submit():
        category_data = Category(category_name=form.category_name.data,
                                 alias=form.alias.data, sous=form.sous.data, cafe=form.cafe.data)
        db.session.add(category_data)
        db.session.commit()
        flash(u'Категория добавлена', "success")
        return redirect(url_for('get_category'))
    return render_template('category_add.html', form=form)


@app.route('/panel/category/tea_category_add', methods=['GET', 'POST'])
def tea_category_add():
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    form = TeaCategoryForm()
    if form.validate_on_submit():
        filename = secure_filename(form.img.data.filename)
        category_data = TeaCategory(tea_category_name=form.tea_category_name.data,
                                    tea_img=form.tea_category_name.data + filename)
        form.img.data.save(basedir + "/static/upload/" + form.tea_category_name.data + filename)
        db.session.add(category_data)
        db.session.commit()
        flash(u'Категория добавлена', "success")
        return redirect(url_for('get_category'))
    return render_template('tea_category_add.html', form=form)


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
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

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
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

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


@app.route('/update_tea_category/<int:category_id>', methods=['GET', 'POST'])
def update_tea_category(category_id):
    """
    Переименовуем категорию
    :rtype : flash
    """
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    select_item = TeaCategory.query.filter_by(id=category_id).first()
    img = select_item.tea_img

    form = TeaCategoryForm(obj=TeaCategory.query.filter_by(id=category_id).first())
    if form.validate_on_submit():
        filename = secure_filename(form.img.data.filename)

        if filename:
            item = TeaCategory.query.get(category_id)
            item.tea_category_name = form.tea_category_name.data
            item.tea_img = form.tea_category_name.data + filename
            form.img.data.save(basedir + "/static/upload/" + form.tea_category_name.data + filename)
            db.session.commit()
        else:
            item = TeaCategory.query.get(category_id)
            item.tea_category_name = form.tea_category_name.data
            item.tea_img = img
            db.session.commit()

        flash(u"Категория " + select_item.tea_category_name + u" Изменена", "info")
        return redirect(url_for("get_tea_category"))

    return render_template("tea_category_edit.html", form=form, img=img)


@app.route('/delete_tea_category/<int:category_id>')
def delete_tea_category(category_id):
    """
    Удаляем категорию
    :rtype : redirect to category page
    """
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    category = TeaCategory.query.get(category_id)
    TeaCategory.query.filter_by(id=category_id).delete()
    db.session.commit()
    flash("Удалена категория - " + category.category_name, "success")

    return redirect(url_for("get_tea_category"))


def jsontostr(table):
    table = json.loads(table)
    ids = 1
    new_table = u"<table border='1'><tr><th>ID</th><th>Название</th><th>Соус</th><th>Количество</th><th>Стоимость</th></tr>"
    for item in table:
        temp_rows = item['row']
        sous = temp_rows[1] if temp_rows[1] != None else u''
        this_row = "<tr>" + "<td>" + str(ids) + "</td>" + "<td>" + temp_rows[0] + u'</td><td>' + sous + u'</td><td>' + \
                   temp_rows[2] + u'</td>' + temp_rows[3] + '</tr>'
        new_table += this_row
        ids += 1

    new_table += u"</table>"
    return new_table


def checkpayments(form_value, price):
    if form_value <= price:
        return True
    else:
        return False


@app.route('/order', methods=['GET', 'POST'])
def order():
    select_item = None
    if current_user.id is None:
        form1 = OrdernoAuchForForDeliveryInCafe()
        form2 = OrdernoAuchForForDeliveryMySelf()
        form3 = OrdernoAuchForDeliveryInHome()
    else:
        select_item = Adress.query.filter_by(user_id=current_user.id).first()
        form1 = OrderAuchForForDeliveryInCafe()
        form2 = OrderAuchForForDeliveryMySelf()
        form3 = OrderAuchForDeliveryInHome(obj=select_item)
        # is_choise = [(g.address, g.address) for g in Adress.query.order_by('address')]
        # is_choise.insert(0, (0,u"Выберите адресс/Либо заполните поля ниже"))
        # form3.select_from_address.choices = is_choise

    delivery = request.cookies.get('delivery')
    if delivery == "deliveryincafe":
        form = form1
    elif delivery == "deliverymyself":
        form = form2
    elif delivery == "deliveryinhome":
        form = form3
    else:
        form = form3

    if form.validate_on_submit():
        if current_user.id == None:
            if form.hidden_type.data == "deliveryinhome":
                if not checkpayments(float(form.select_region.data), float(request.cookies.get('cart_price'))):
                    flash(u"Сумма заказа в данный район должна быть больше " + str(form.select_region.data) + 'руб.',
                          'info')
                    return redirect('order')
                else:
                    msg = MIMEMultipart()
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = "Ваш Заказ с сайта Sir Vincenzo "

                    message = """
                    <div><strong>Заказ с сайта:</strong> на дом
                    <br><strong> Имя:</strong> {}
                    <br><strong>Дата время заказа:</strong>{}
                    <br><strong> Промокод:</strong>{}
                    <br><strong> Телефон:</strong>  {}
                    <br><strong> Регион:</strong>  {}
                    <br><strong> Улица:</strong>  {}
                    <br><strong> Дом:</strong>  {}
                    <br><strong> Корпус/Строеие:</strong> {}
                    <br><strong> Подъезд: </strong> {}
                    <br><strong> Домофон:</strong> {}
                    <br><strong> Этаж:</strong> {}
                    <br><strong> Квартира:</strong> {}
                    <br><strong>Количество персон(приборов):</strong> {}
                    <br><strong> Способ оплаты:</strong> {}
                    <br><strong> Сдача с суммы:</strong> {}
                    <br><strong> Заказ на дату/время:</strong> {}
                    <br><strong> Дополнительная информация:</strong> {}
                    <br><strong> Заказ:</strong><br>{}
                    <br><strong>Общая сумма заказа:</strong><br><h3>{} Рублей</h3> +
                    </div>""".format(form.name.data, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                     form.promo.data, str(form.phone.data), selectdeliveretext(form.select_region.data),
                                     form.street.data, form.home.data, form.home_corp.data, form.porch.data,
                                     form.domofon.data,
                                     form.floor.data, form.kvartira.data, form.person.data, form.pey_method.data,
                                     form.hiden_sdacha.data, form.delivery_time.data, form.some_info.data,
                                     jsontostr(form.hidden_table.data), form.hidden_full_cost.data)
                msg.attach(MIMEText(message.encode('utf-8'), 'html'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, mypass)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                text = ""
                return redirect(url_for('ordercomplete'))

            if form.hidden_type.data == "deliveryincafe":
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "Ваш Заказ с сайта Sir Vincenzo "

                message = """
                <div><strong>Заказ с сайта</strong>:в кафе
                <br><strong>Имя:</strong> {}
                <br><strong>Дата время заказа:</strong> {}
                <br><strong> Промокод:</strong> {}
                <br> <strong>Телефон:</strong> {}
                <br> <strong>Заказ на дату/время:</strong>  {}
                <br> <strong>Дополнительная информация:</strong> {}
                <br> <strong>Заказ:</strong><br> {}
                <br><strong>Общая сумма заказа:</strong><br><h3>  {}  Рублей</h3>
                <br> <strong>Дополнительная информация о заказе:</strong>  {}
                </div>""".format(form.name.data, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), form.promo.data,
                                 str(form.phone.data), form.delivery_time.data, form.some_info.data,
                                 jsontostr(form.hidden_table.data), form.hidden_full_cost.data,
                                 form.hidden_allaboutorder.data)

                msg.attach(MIMEText(message.encode('utf-8'), 'html'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, mypass)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                text = ""
                return redirect(url_for('ordercomplete'))

            if form.hidden_type.data == "deliverymyself":
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "Ваш Заказ с сайта Sir Vincenzo "

                message = """
                    <div><strong>Заказ с сайта. в самовывоз :</strong> {}
                            <br><strong>Дата время заказа:</strong> {}
                            <br><strong> Промокод:</strong> {}
                            <br> <strong>Телефон:</strong> {}
                            <br> <strong>Заказ на дату/время:</strong> {}
                            <br> <strong>Дополнительная информация:</strong> {}
                            <br> <strong>Заказ:</strong> <br> {}
                            <br><strong>Общая сумма заказа:</strong><br><h3>  {} Рублей</h3>
                            <br> <strong>Дополнительная информация о заказе:</strong>  {}
                    </div>""".format(form.name.data,
                                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                     form.promo.data, str(form.phone.data), form.delivery_time.data,
                                     form.some_info.data,
                                     jsontostr(form.hidden_table.data), form.hidden_full_cost.data,
                                     form.hidden_allaboutorder.data)
                msg.attach(MIMEText(message.encode('utf-8'), 'html'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, mypass)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                text = ""
                return redirect(url_for('ordercomplete'))

        elif current_user.id != None:
            if form.hidden_type.data == "deliveryinhome":
                if not checkpayments(float(form.select_region.data), float(request.cookies.get('cart_price'))):
                    flash(u"Сумма заказа в данный район должна быть больше " + str(form.select_region.data) + 'руб.',
                          'info')
                    return redirect('order')
                else:
                    msg = MIMEMultipart()
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = "Ваш Заказ с сайта Sir Vincenzo "

                    message = """
                            <div><strong>Зарегистрированный пользователь.</strong>{}
                                     {}
                                   <br><strong>Дата время заказа:</strong> {}
                                   <br><strong>Заказ с сайта:</strong> на дом
                                   <br><strong>Имя пользователя:</strong>  {}
                                   <br><strong> Промокод:</strong>{}
                                   <br><strong>Телефон:</strong>{}
                                   <br><strong>Регион:</strong>{}
                                   <br><strong>Улица:</strong>{}
                                   <br><strong>Дом:</strong>{}
                                   <br><strong>Корпус/Строеие</strong>:{}
                                   <br><strong>Подъезд:</strong> {}
                                   <br><strong>Домофон</strong>{}
                                   <br><strong>Этаж:</strong>{}
                                   <br><strong>Квартира:</strong>{}
                                   <br><strong>Количество персон(приборов)</strong>:{}
                                   <br><strong>Способ оплаты</strong>:{}
                                   <br><strong>Сдача с суммы</strong:>{}
                                   <br><strong>Заказ на дату/время:</strong> {}
                                   <br><strong>Дополнительная информация:</strong> {}
                                   <br><strong>Заказ:</strong><br>{}
                                   <br><strong>Общая сумма заказа:</strong><br><h3> {} Рублей</h3>
                                   <br> <strong>Дополнительная информация о заказе:</strong>{}
                                   </div>""".format(current_user.username, firstorder(),
                                                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                    current_user.username, form.promo.data, str(current_user.phone),
                                                    selectdeliveretext(form.select_region.data), form.street.data,
                                                    form.home.data,
                                                    form.home_corp.data, form.porch.data, form.domofon.data,
                                                    form.floor.data,
                                                    form.kvartira.data, form.person.data, form.pey_method.data,
                                                    form.hiden_sdacha.data, form.delivery_time.data,
                                                    form.some_info.data,
                                                    jsontostr(form.hidden_table.data), form.hidden_full_cost.data,
                                                    form.hidden_allaboutorder.data)

                    user_address = Adress.query.filter_by(user_id=current_user.id).first()
                    if user_address is None:
                        address_data = Adress(
                            user_id=current_user.id,
                            select_region=form.select_region.data,
                            street=form.street.data,
                            home=form.home.data,
                            home_corp=form.home_corp.data,
                            porch=form.porch.data,
                            domofon=form.domofon.data,
                            floor=form.floor.data,
                            kvartira=form.kvartira.data
                        )
                        db.session.add(address_data)
                        db.session.commit()
                    else:
                        db.session.query(Adress).filter(Adress.user_id == current_user.id).update(
                            {'select_region': form.select_region.data,
                             'street': form.street.data,
                             'home': form.home.data,
                             'home_corp': form.home_corp.data,
                             'porch': form.porch.data,
                             'domofon': form.domofon.data,
                             'floor': form.floor.data,
                             'kvartira': form.kvartira.data
                             })
                        db.session.commit()

                    msg.attach(MIMEText(message.encode('utf-8'), 'html'))
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(fromaddr, mypass)
                    text = msg.as_string()
                    server.sendmail(fromaddr, toaddr, text)
                    server.quit()
                    text = ""
                    return redirect(url_for('ordercomplete'))

            if form.hidden_type.data == "deliveryincafe":
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "Ваш Заказ с сайта Sir Vincenzo "

                message = """
                        <div><strong>Зарегистрированный пользователь.</strong> {}
                                {}
                                <br><strong>Дата время заказа:</strong>{}
                                <br><strong>Заказ с сайта: </strong>:в кафе
                                <br><strong> Промокод:</strong> {}
                                <br><strong>Телефон:</strong>{}
                                <br>Заказ на дату/время:</strong> {}
                                <br><strong>Дополнительная информация:</strong> {}
                                <br><strong>Заказ:</strong><br>{}
                                <br><strong>Общая сумма заказа:</strong><br><h3> {} Рублей</h3>
                                <br> <strong>Дополнительная информация о заказе:</strong> {}
                                </div>""".format(current_user.username, firstorder(),
                                                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), form.promo.data,
                                                 str(current_user.phone), form.delivery_time.data, form.some_info.data,
                                                 jsontostr(form.hidden_table.data), form.hidden_full_cost.data,
                                                 form.hidden_allaboutorder.data)
                msg.attach(MIMEText(message.encode('utf-8'), 'html'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, mypass)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                text = ""
                return redirect(url_for('ordercomplete'))

            if form.hidden_type.data == "deliverymyself":
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "Ваш Заказ с сайта Sir Vincenzo "

                message = """
                   <div>Зарегистрированный пользователь.<br>Заказ с сайта. самовывоз :' {}
                            {}
                            <br><strong>Дата время заказа:</strong>{}
                            <br><strong> Промокод:</strong>{}
                            <br> Телефон:{}
                            <br> Заказ на дату/время: {}
                            <br> Дополнительная информация:{}
                            <br> Заказ <br>{}
                            <br><strong>Общая сумма заказа:</strong><br><h3> {} Рублей</h3>
                            <br> <strong>Дополнительная информация о заказе:</strong> {}
                            </div>""".format(current_user.username, firstorder(),
                                             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), form.promo.data,
                                             str(current_user.phone), form.delivery_time.data, form.some_info.data,
                                             jsontostr(form.hidden_table.data), form.hidden_full_cost.data,
                                             form.hidden_allaboutorder.data)

                msg.attach(MIMEText(message.encode('utf-8'), 'html'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, mypass)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                text = ""
                return redirect(url_for('ordercomplete'))

    else:
        settings_it = [str("delete_buy_button"), str(delivery)]
        resp = make_response(render_template("order.html", form=form, title="Vincenzo", settings_order=settings_it))
        resp.set_cookie('localLinkClicked', 'true')
        return resp


@app.route('/deliveryinhome', methods=["POST", "GET"])
def post_deliveryinhome():
    form = OrdernoAuchForDeliveryInHome()
    if form.validate():
        flash(u"Заказ оформлен deliveryinhome", 'success')
        return redirect(url_for('order'))
    return redirect(url_for('order'))


@app.route('/get_one_item1/<int:item_id>', methods=['GET', 'POST'])
def get_one_item1(item_id):
    delivery = request.cookies.get('delivery')
    select_item = db.session.query(Items, Category).filter_by(id=item_id). \
        join(Category, Items.category_id == Category.id).first()
    # select_item = Items.query.
    # return jsonify(result=dict(item_id=select_item[0].id,
    #                            name=select_item[0].item_name,
    #                            imgs=select_item[0].img,
    #                            components=select_item[0].item_component,
    #                            weight=select_item[0].weight,
    #                            price=select_item[0].price,
    #                            cafe_only=select_item[0].cafe_only,
    #                            category=select_item[1].category_name,
    #                            sous=select_item[1].sous
    #                            )
    #
    #                )
    buyactioncontent = '{'+'"item_id":"{0}","item_name":"{1}","item_price":"{2}","item_component":"{3}","item_weight":"{4}","item_category":"{5}","sous":"{6}"'.format(
        select_item[0].id,
        select_item[0].item_name,
        select_item[0].price,
        select_item[0].item_component,
        select_item[0].weight,
        select_item[1].category_name,
        select_item[1].sous
    )+'}'
    return render_template('popUp.html',
                           item=select_item,
                           buyactioncontent=buyactioncontent,
                           delivery=delivery
                           )


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
    return render_template('sale.html', sales=select_sales)


@app.route('/one_sale/<int:sale_id>', methods=['GET', 'POST'])
def one_sale(sale_id):
    one_sales = db.session.query(Sale).filter_by(id=sale_id).first()
    return render_template('one_sale.html', sale=one_sales)


@app.route('/aboutus', methods=['GET', 'POST'])
def about_us():
    return render_template("aboutus.html", title="О нас")


@app.route('/panel/item_add', methods=['GET', 'POST'])
def item_add():
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

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
            thumbnail=form.item_name.data + "thumbnail" + thumbnail,
            isportret=form.isportret.data
        )
        db.session.add(item_data)
        db.session.commit()
        form.img.data.save(basedir + "/static/upload/" + form.item_name.data + filename)
        form.thumbnail.data.save(basedir + "/static/upload/" + form.item_name.data + "thumbnail" + thumbnail)
        flash("Добавлен новый товар", "success")
        return redirect(url_for("items"))

    return render_template('items_add.html', form=form)


@app.route('/panel/tea_item_add', methods=['GET', 'POST'])
def tea_item_add():
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    form = TeaForm()
    form.tea_category_id.choices = [(c.id, c.tea_category_name) for c in TeaCategory.query.all()]
    if request.method == 'POST':
        item_data = Tea(
            tea_name=form.tea_name.data,
            tea_category_id=form.tea_category_id.data,
            tea_about=form.tea_about.data,
            tea_price_400=form.tea_price_400.data,
            tea_price_800=form.tea_price_800.data,
            tea_price_1000=form.tea_price_1000.data
        )
        db.session.add(item_data)
        db.session.commit()

        flash("Добавлен новый Чай", "success")
        return redirect(url_for("tea_items"))

    return render_template('tea_items_add.html', form=form)


@app.route('/panel/tea_item_edit/<int:item_id>', methods=['GET', 'POST'])
def tea_item_edit(item_id):
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    select_item = Tea.query.filter_by(id=item_id).first()
    form = TeaForm(obj=select_item)
    form.tea_category_id.choices = [(c.id, c.tea_category_name) for c in TeaCategory.query.all()]
    if form.validate_on_submit():
        item = Tea.query.get(item_id)
        item.tea_category_id = form.tea_category_id.data
        item.tea_name = form.tea_name.data
        item.tea_about = form.tea_about.data
        item.tea_price_400 = form.tea_price_400.data
        item.tea_price_800 = form.tea_price_800.data
        item.tea_price_1000 = form.tea_price_1000.data
        db.session.commit()

        flash(u"Изменено", "info")
        return redirect(url_for("tea_items"))

    return render_template('tea_items_edit.html', form=form)


@app.route('/panel/item_edit/<int:item_id>', methods=['GET', 'POST'])
def item_edit(item_id):
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

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
            item.isportret = form.isportret.data
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
            item.isportret = form.isportret.data
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
            item.isportret = form.isportret.data
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
            item.isportret = form.isportret.data
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
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    item = Items.query.get(item_id)
    Items.query.filter_by(id=item_id).delete()
    db.session.commit()
    flash("Удален - " + item.item_name, "success")
    return redirect(url_for("items"))


@app.route('/panel/items', methods=['GET', 'POST'])
def items():
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    all_items = db.session.query(Items, Category).join(Category, Items.category_id == Category.id).all()
    return render_template("items.html", items=all_items)


@app.route('/panel/tea_items', methods=['GET', 'POST'])
def tea_items():
    if not session.get('logged_in'):
        return redirect(url_for("adminlogin"))

    all_items = db.session.query(Tea, TeaCategory).join(TeaCategory, Tea.tea_category_id == TeaCategory.id).all()
    return render_template("tea_items.html", items=all_items)


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
    msg = MIMEMultipart()
    new_password = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
    message = """<p>Ваш новый пароль для сайта vincenzo-pizza.com: {}</p> """.format(new_password)
    user = User.query.get(is_user.id)
    user.password = new_password
    db.session.commit()
    msg['To'] = is_user.email
    msg['Subject'] = "Востановление пароля сайта Sir Vincenzo "
    msg.attach(MIMEText(message.encode("utf-8"), 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, is_user.email, text)
    server.quit()
    result = "sent"
    return jsonify(result=result)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    phone=form.phone.data,
                    authenticated=True)
        db.session.add(user)
        db.session.commit()
        registered_user = User.query.filter_by(phone=form.phone.data,
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


@app.route('/tea', methods=['GET'])
def tea():
    select_category = TeaCategory.query.all()

    return render_template("tea.html", tea_category=select_category,
                           title="Vincenzo")


@app.route('/tea/<int:category_id>', methods=['GET'])
def tea_one(category_id):
    select_category = TeaCategory.query.filter_by(id=category_id).one()
    select_item = db.session.query(Tea).filter_by(tea_category_id=category_id).all()
    return render_template("teaone.html", select_category=select_category, tea_select=select_item,
                           title="Vincenzo")


@app.route('/ordercomplete', methods=['GET'])
def ordercomplete():
    if current_user.id is not None:
        db.session.query(User).filter(User.id == current_user.id).update(
            {'first_order': False})
        db.session.commit()
    resp = make_response(render_template("order_complete.html", title="Vincenzo"))
    resp.set_cookie('localLinkClicked', 'true')
    return resp





    # elif form.hidden_type.data == "deliveryinhome" and form.select_from_address.data == 0 and current_user.id is not None:
    #     if form.validate_on_submit():
    #         try:
    #             mandrill_client = mandrill.Mandrill('wv39DASQNMJbfCratNJa2w')
    #             message = {
    #                 'auto_html': True,
    #                 'auto_text': None,
    #                 'from_email': 'sir.vincenzo.office@gmail.com',
    #                 'from_name': 'Sir Vincenzo ',
    #                 'headers': {'Reply-To': 'sir.vincenzo.office@gmail.com'},
    #                 'html': '<div>Заказ с сайта. на дом :' + form.name.data +
    #                         '<br> Телефон:' + str(form.phone.data) +
    #                         '<br> Регион:' + form.select_region.data +
    #                         '<br> Улица:' + form.street.data +
    #                         '<br> Дом:' + form.home.data +
    #                         '<br> Корпус/Строеие' + form.home_corp.data +
    #                         '<br> Подъезд: ' + form.porch.data +
    #                         '<br> Домофон' + form.domofon.data +
    #                         '<br> Этаж:' + form.floor.data +
    #                         '<br> Квартира:' + form.kvartira.data +
    #                         'Количество персон(приборов)' + form.person.data +
    #                         '<br> Способ оплаты' + form.pey_method.data +
    #                         '<br> Сдача с суммы' + form.hiden_sdacha.data +
    #                         '<br> Заказ на дату/время' + form.delivery_time.data +
    #                         '<br> Дополнительная информация' + form.some_info.data +
    #                         '<br> Заказ:<br>' + ''.join(jsontostr(form.hidden_table.data)) +
    #                         '</div>',
    #                 'subject': 'Ваш Заказ с сайта Sir Vincenzo ',
    #                 'to': [{'email': "sir.vincenzo.office@gmail.com",
    #                         'name': "serdimoa",
    #                         'type': 'to'}]
    #             }
    #             result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
    #             return redirect(url_for('ordercomplete'))
    #         except mandrill.Error, e:  # Mandrill errors are thrown as exceptions
    #             return jsonify(result=2)
    #
    # # elif request.method=='POST' and form.hidden_type.data == "deliveryinhome" and form.select_from_address.data != 0 and current_user.id is not None:
    # #         flash(form.select_from_address.data,category='info')
    # #         return redirect(url_for('order'))
    #
    # elif form.validate_on_submit() and form.hidden_type.data != "deliveryinhome" and current_user.id is not None:
    #     if form.hidden_type.data == "deliveryincafe":
    #         try:
    #             mandrill_client = mandrill.Mandrill('wv39DASQNMJbfCratNJa2w')
    #             message = {
    #                 'auto_html': True,
    #                 'auto_text': None,
    #                 'from_email': 'sir.vincenzo.office@gmail.com',
    #                 'from_name': 'Sir Vincenzo ',
    #                 'headers': {'Reply-To': 'sir.vincenzo.office@gmail.com'},
    #                 'html': '<div>Заказ с сайта. в кафе :' + form.name.data +
    #                         '<br> Телефон:' + str(form.phone.data) +
    #                         '<br> Заказ на дату/время:' + form.delivery_time.data +
    #                         '<br> Дополнительная информация:' + form.some_info.data +
    #                         '<br> Заказ:<br>' + ''.join(jsontostr(form.hidden_table.data)) +
    #                         '</div>',
    #                 'subject': 'Ваш Заказ с сайта Sir Vincenzo ',
    #                 'to': [{'email': "sir.vincenzo.office@gmail.com",
    #                         'name': "serdimoa",
    #                         'type': 'to'}]
    #             }
    #             result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
    #             return redirect(url_for('ordercomplete'))
    #         except mandrill.Error, e:  # Mandrill errors are thrown as exceptions
    #             return jsonify(result=2)
    #     if form.hidden_type.data == "deliverymyself":
    #         try:
    #             mandrill_client = mandrill.Mandrill('wv39DASQNMJbfCratNJa2w')
    #             message = {
    #                 'auto_html': True,
    #                 'auto_text': None,
    #                 'from_email': 'sir.vincenzo.office@gmail.com',
    #                 'from_name': 'Sir Vincenzo ',
    #                 'headers': {'Reply-To': 'sir.vincenzo.office@gmail.com'},
    #                 'html': '<div>Заказ с сайта. в самовывоз :' + form.name.data +
    #                         '<br> Телефон ' + str(form.phone.data) +
    #                         '<br> Заказ на дату/время' + form.delivery_time.data +
    #                         '<br> Дополнительная информация' + form.some_info.data +
    #                         '<br> Заказ <br>' + ''.join(jsontostr(form.hidden_table.data)) +
    #                         '</div>',
    #                 'subject': 'Ваш Заказ с сайта Sir Vincenzo ',
    #                 'to': [{'email': "sir.vincenzo.office@gmail.com",
    #                         'name': "serdimoa",
    #                         'type': 'to'}]
    #             }
    #             result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
    #             return redirect(url_for('ordercomplete'))
    #         except mandrill.Error, e:  # Mandrill errors are thrown as exceptions
    #             return jsonify(result=2)
