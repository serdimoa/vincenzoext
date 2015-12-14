# coding=utf-8
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField
from wtforms import StringField, BooleanField, SelectField, IntegerField
from wtforms.validators import Required


class LoginForm(Form):
    openid = StringField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class ItemForm(Form):
    item_name = StringField(u"Наименование")
    item_component = StringField(u"Компоненты")
    category_id = SelectField(u"Категория", coerce=int)
    weight = IntegerField(u"Вес")
    price = IntegerField(u"Цена")
    img = FileField(u"Изображение")


class CategoryForm(Form):
    category_name = StringField(u"Имя категории")
    alias = StringField("alias")
