from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    HiddenField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
)
from wtforms.validators import DataRequired, EqualTo, NumberRange, Optional


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[Optional()])
    name = StringField('Имя', validators=[Optional()])
    patronymic = StringField('Отчество', validators=[Optional()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField(
        'Подтвердите пароль',
        validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')],
    )
    address = StringField('Адрес доставки', validators=[Optional()])


class ActionForm(FlaskForm):
    pass


class ProfileForm(FlaskForm):
    id = HiddenField()
    name = StringField('Имя', validators=[Optional()])
    surname = StringField('Фамилия', validators=[Optional()])
    patronymic = StringField('Отчество', validators=[Optional()])
    login = StringField('Логин', validators=[DataRequired()])
    address = StringField('Адрес доставки', validators=[Optional()])
    current_password = PasswordField('Текущий пароль', validators=[Optional()])
    new_password = PasswordField('Новый пароль', validators=[Optional()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[Optional()])


class ProductForm(FlaskForm):
    id = HiddenField()
    name = StringField('Название', validators=[DataRequired()])
    dosage = StringField('Дозировка', validators=[Optional()])
    category = SelectField(
        'Категория',
        choices=[
            ('Лекарства', 'Лекарства'),
            ('Витамины и БАД', 'Витамины и БАД'),
            ('Красота', 'Красота'),
            ('Гигиена', 'Гигиена'),
        ],
        validators=[Optional()],
    )
    price = FloatField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    in_stock = SelectField(
        'Наличие',
        choices=[(1, 'Есть в наличии'), (0, 'Нет в наличии')],
        coerce=int,
    )


class AdminUserForm(FlaskForm):
    id = HiddenField()
    surname = StringField('Фамилия', validators=[Optional()])
    name = StringField('Имя', validators=[Optional()])
    patronymic = StringField('Отчество', validators=[Optional()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[Optional()])
    confirm = PasswordField('Подтвердите пароль', validators=[Optional()])
    address = StringField('Адрес доставки', validators=[Optional()])
    is_admin = SelectField(
        'Роль',
        choices=[(0, 'Пользователь'), (1, 'Администратор')],
        coerce=int,
    )


class OrderForm(FlaskForm):
    id = HiddenField()
    user_id = HiddenField()
    product_ids = SelectMultipleField('Товары', coerce=int, validators=[Optional()])
    payment = SelectField(
        'Способ оплаты',
        choices=[('наличные', 'Наличные')],
    )
