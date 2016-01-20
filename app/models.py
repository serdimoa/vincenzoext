from app import db
from flask.ext.login import UserMixin, AnonymousUserMixin
from sqlalchemy_utils import PhoneNumberType


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    phone = db.Column(PhoneNumberType(country_code='RU', max_length=20), unique=True)

    def __init__(self, username, email, phone, authenticated, password):
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password
        self.authenticated = authenticated

    def __repr__(self):
        return '<User %r>' % self.username

        # def is_active(self):
        #     """True, as all users are active."""
        #     return True
        #
        # def get_id(self):
        #     """Return the email address to satisfy Flask-Login's requirements."""
        #     return self.username
        #
        # def is_authenticated(self):
        #     """Return True if the user is authenticated."""
        #     return True
        #
        # def is_anonymous(self):
        #     """False, as anonymous users aren't supported."""
        #     return False


class TeaCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tea_category_name = db.Column(db.String(50))
    tea_img = db.Column(db.String(50))

    def __init__(self, tea_category_name, tea_img):
        self.tea_category_name = tea_category_name
        self.tea_img = tea_img

    def __unicode__(self):
        return self.tea_category_name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50))
    alias = db.Column(db.String(50))
    sous = db.Column(db.Boolean, default=False)
    cafe = db.Column(db.Boolean, default=True)

    def __init__(self, category_name, alias, sous, cafe):
        self.category_name = category_name
        self.alias = alias
        self.sous = sous
        self.cafe = cafe

    def __repr__(self):
        return '<Category %r>' % self.category_name

    def __unicode__(self):
        return self.category_name


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50))
    item_component = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    weight = db.Column(db.String(50))
    price = db.Column(db.String(50), default=0)
    img = db.Column(db.String(50))
    thumbnail = db.Column(db.String(255))
    cafe_only = db.Column(db.Boolean)

    def __unicode__(self):
        return self.item_name

    def __init__(self, item_name, item_component, category_id, weight, price, img, thumbnail, cafe_only):
        self.item_name = item_name
        self.item_component = item_component
        self.category_id = category_id
        self.weight = weight
        self.price = price
        self.img = img
        self.thumbnail = thumbnail
        self.cafe_only = cafe_only

    def __repr__(self):
        return '<Item %r>' % self.item_name


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.Column(db.String(50))
    items_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    def __unicode__(self):
        return self.likes

    def __init__(self, user_id, items_id):
        self.user_id = user_id
        self.items_id = items_id

    def __repr__(self):
        return '<like %r>' % self.items_id


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50))
    admin_password = db.Column(db.String(50))


class Adress(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.Text)

    def __init__(self, user_id, address):
        self.user_id = user_id
        self.address = address


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_name = db.Column(db.String(20))
    price_if_have = db.Column(db.Integer)
    to_slider = db.Column(db.Boolean)
    about_sale = db.Column(db.String(255))
    show_url = db.Column(db.Boolean)
    end_sale = db.Column(db.Date)
    img = db.Column(db.String(50))

    def __init__(self, sale_name, price_if_have, to_slider, about_sale, show_url, end_sale, img):
        self.sale_name = sale_name
        self.price_if_have = price_if_have
        self.to_slider = to_slider
        self.about_sale = about_sale
        self.show_url = show_url
        self.end_sale = end_sale
        self.img = img


class SaleoOnTime(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_name = db.Column(db.String(255))
    down_sale = db.Column(db.String(20))
    date_sale_on = db.Column(db.String(255))
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)

    def __init__(self, sale_name, down_sale, date_sale_on, time_start, time_end):
        self.sale_name = sale_name
        self.down_sale = down_sale
        self.date_sale_on = date_sale_on
        self.time_start = time_start
        self.time_end = time_end

    def to_json(self):
        return dict(sale_name=self.sale_name,
                    down_sale=self.down_sale,
                    date_sale_on=self.date_sale_on,
                    time_start=self.time_start,
                    time_end=self.time_end)


class Tea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tea_category_id = db.Column(db.Integer, db.ForeignKey('teacategory.id'))
    tea_name = db.Column(db.String(20))
    tea_about = db.Column(db.String(255))
    tea_price_400 = db.Column(db.Integer)
    tea_price_800 = db.Column(db.Integer)
    tea_price_1000 = db.Column(db.Integer)

    def __init__(self, tea_name, tea_category_id, tea_about, tea_price_400, tea_price_800, tea_price_1000):
        self.tea_category_id = tea_category_id
        self.tea_name = tea_name
        self.tea_about = tea_about
        self.tea_price_400 = tea_price_400
        self.tea_price_800 = tea_price_800
        self.tea_price_1000 = tea_price_1000


class AnonymousUser(AnonymousUserMixin):
    id = None
