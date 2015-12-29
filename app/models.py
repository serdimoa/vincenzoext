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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50))
    alias = db.Column(db.String(50))

    def __init__(self, category_name, alias):
        self.category_name = category_name
        self.alias = alias

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

    def __unicode__(self):
        return self.item_name

    def __init__(self, item_name, item_component, category_id, weight, price, img):
        self.item_name = item_name
        self.item_component = item_component
        self.category_id = category_id
        self.weight = weight
        self.price = price
        self.img = img

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
    adress = db.Column(db.String(50))


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_name = db.Column(db.String(20))
    price_if_have = db.Column(db.Integer)
    to_slider = db.Column(db.Boolean)
    about_sale = db.Column(db.String(255))
    show_url = db.Column(db.Boolean)
    img = db.Column(db.String(50))


class AnonymousUser(AnonymousUserMixin):
    id = None
