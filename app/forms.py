# coding=utf-8
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField
from wtforms import StringField, BooleanField, SelectField, IntegerField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required
from wtforms import validators
from models import User
from wtforms.validators import ValidationError
from wtforms_components import PhoneNumberField


class PhoneNumber(PhoneNumberField):
    """
    A string field representing a PhoneNumber object from
    `SQLAlchemy-Utils`_.

    .. _SQLAlchemy-Utils:
       https://github.com/kvesteri/sqlalchemy-utils

    :param country_code:
        Country code of the phone number.
    :param display_format:
        The format in which the phone number is displayed.
    """
    error_msg = u'Вы ввели не коректный телефон'


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


class UserEdit(Form):
    username = StringField(u"Ваш email")
    phone = PhoneNumber(u"Ваш телефон", country_code='RU', display_format='e164', validators=[validators.Optional()])


class RegistrationForm(Form):
    username = StringField(u"Ваше имя", validators=[validators.InputRequired(u"Введите Ваше имя")])
    email = EmailField(u"Ваш email", validators=[validators.InputRequired(u"Введите Email"), Unique(
        User, User.email, message=u"Такой email существует")])
    password = PasswordField(u"Ваш пароль", validators=[validators.InputRequired(u"Введите Ваш пароль")])
    phone = PhoneNumber(u"Ваш телефон",country_code='RU', display_format='e164', validators=[validators.InputRequired(u"Введите Ваш телефон"), Unique(
        User, User.phone, message=u"Такой телефон существует"), validators.Optional()])


class CategoryForm(Form):
    category_name = StringField(u"Имя категории")
    alias = StringField("alias")
