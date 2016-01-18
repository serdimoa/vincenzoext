# coding=utf-8
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField
from wtforms import StringField, BooleanField, SelectField, IntegerField, PasswordField, SubmitField, TextAreaField, \
    SelectMultipleField, HiddenField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import Required
from wtforms import validators
from models import User
from wtforms.validators import ValidationError
from wtforms_components import PhoneNumberField, TimeField
import datetime

weaks = [('0', u'Воскресенье'), ('1', u'Понедельник'), ('2', u'Вторник'), ('3', u'Среда'), ('4', u'Четверг'),
         ('5', u'Пятница'), ('6', u'Суббота')]

delivery_price = [('500', u'По городу'), ('800', u'Пром.зона'), ('800', u'Старый Вартовск (район Энтузиастов'),
                  ('1000', u'Старый Вартовск (район "Горбатый")'), ('1200', u'Старый Вартовск (район "ЛПХ"и далее)'),
                  ('1500', u'Излучинск')]


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


class Integers(IntegerField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                self.data = None
                raise ValueError(self.gettext(u'Должно быть числом'))


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
    cafe_only = BooleanField(u"Только в кафе?")
    img = FileField(u"Изображение")
    thumbnail = FileField(u"Миниатюра")


class UserEdit(Form):
    username = StringField(u"Ваше имя")
    phone = PhoneNumber(u"Ваш телефон", country_code='RU', display_format='e164',
                        validators=[validators.Optional(),
                                    Unique(User, User.phone, message=u"Такой телефон существует")])


class ChangeUserPassword(Form):
    old_password = PasswordField(u"Ваш старый пароль")
    new_password = StringField(u"Ваш новый пароль")


class RegistrationForm(Form):
    username = StringField(u"Ваше имя", validators=[validators.InputRequired(u"Введите Ваше имя")])
    email = EmailField(u"Ваш email", validators=[validators.InputRequired(u"Введите Email"), Unique(
        User, User.email, message=u"Такой email существует")])
    password = PasswordField(u"Ваш пароль",
                             validators=[validators.InputRequired(u"Введите Ваш пароль"),
                                         validators.EqualTo('confirm', message=u'Пароли должны совпадать')])
    confirm = PasswordField(u'Повторите парль')
    phone = PhoneNumber(u"Ваш телефон", country_code='RU', display_format='e164',
                        validators=[validators.InputRequired(u"Введите Ваш телефон"), Unique(
                            User, User.phone, message=u"Такой телефон существует"), validators.Optional()])


class AuchForm(Form):
    login = PhoneNumber(u"Телефон", validators=[validators.InputRequired(u"Введите Ваш телефон")])
    password = PasswordField(u"Пароль", validators=[validators.InputRequired(u"Введите Ваш пароль")])


class SaleAddForm(Form):
    sale_name = StringField(u"Название Акции", validators=[validators.InputRequired(u"Введите Название")])
    end_sale = DateField(u"Дата окончания", format='%Y-%m-%d')
    price_if_have = Integers(u"Цена если требуется", validators=[validators.Optional()])
    about_sale = TextAreaField(u"Информация об акции")
    show_url = BooleanField(u"Покаывать кнопку или нет")
    to_slider = BooleanField(u"Покаывать в слайдере ")
    img = FileField(u"Изображение")


b = datetime.timedelta(hours=2, minutes=30)


class ordernoAuch(Form):
    name = StringField(u"Ваше имя*", validators=[validators.InputRequired(u"Введите Ваше имя")])
    phone = PhoneNumber(u"Телефон*", validators=[validators.InputRequired(u"Введите Ваш телефон")])
    select_region = SelectField(u"Выберите раен доставки", choices=delivery_price)
    street = StringField(u"Улица*", validators=[validators.InputRequired(u"Введите Вашу улицу")])
    home = StringField(u"Дом*", validators=[validators.InputRequired(u"Введите Ваш дом")])
    home_corp = StringField(u"Корпус/строение")
    porch = StringField(u"Подъезд*", validators=[validators.InputRequired(u"Введите Ваш подъезд")])
    domofon = StringField(u"Домофон*", validators=[validators.InputRequired(u"Это поле обязательно для заполнения")])
    floor = StringField(u"Этаж*", validators=[validators.InputRequired(u"Это поле обязательно для заполнения")])
    kvartira = StringField(u"Квартира*", validators=[validators.InputRequired(u"Это поле обязательно для заполнения")])
    delivery = DateField(u"Заказ на дату")
    delivery_time = TimeField(u"Заказ на время")
    hiden_zdacha = HiddenField(u"Здача")


class CategoryForm(Form):
    category_name = StringField(u"Имя категории")
    alias = StringField("")
    sous = BooleanField(u"Покаывать соусы в корзине или нет")
    cafe = BooleanField(u"Покаывать кнопку купить или нет")


class SaleOnTimeForm(Form):
    sale_name = StringField(u"Описание")
    down_sale = StringField(u"Скидка в %")
    date_sale_on = SelectMultipleField(u"Дни недели когда активна акция", choices=weaks)
    time_start = TimeField(u"Начало акции(время)")
    time_end = TimeField(u"Конец акции(время)")
