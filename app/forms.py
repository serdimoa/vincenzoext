# coding=utf-8
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField
from wtforms import StringField, BooleanField, SelectField, IntegerField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required
from wtforms import validators
from models import User
from wtforms.validators import ValidationError


class Unique(object):
    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


class LoginForm(Form):
    openid = StringField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class ItemForm(Form):
    item_name = StringField(u"Наименование")
    item_component = StringField(u"Компоненты")
    category_id = SelectField(u"Категория", coerce=int)
    weight = StringField(u"Вес/Объем")
    price = IntegerField(u"Цена")
    img = FileField(u"Изображение")


class RegistrationForm(Form):
    username = StringField(u"Ваше имя", validators=[validators.InputRequired(u"Введите Ваше имя")])
    email = EmailField(u"Ваш email", validators=[validators.InputRequired(u"Введите Email"), Unique(
        User, User.email, message=u"Такой email существует")])
    password = PasswordField(u"Ваш пароль", validators=[validators.InputRequired(u"Введите Ваш пароль")])
    phone = StringField(u"Ваш телефон", validators=[validators.InputRequired(u"Введите Ваш телефон"), Unique(
        User, User.phone, message=u"Такой телефон существует")])


class CategoryForm(Form):
    category_name = StringField(u"Имя категории")
    alias = StringField("alias")
