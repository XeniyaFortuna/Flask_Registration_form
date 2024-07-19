from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo


def password_validator(form, field):
    is_upper = False
    is_lower = False
    is_number = False
    is_special = False
    for symbol in field.data:
        if symbol in 'QWERTYUIOPASDFGHJKLZXCVBNMЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ':
            is_upper = True
        if symbol in 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю':
            is_lower = True
        if symbol.isdigit():
            is_number = True
        if symbol in '!@#$%^&*()_-=+"№;:?':
            is_special = True
    if not (is_upper and is_lower and is_number and is_special):
        raise ValidationError('пароль должен содержать минимум одну большую и одну маленькую букву, '
                              'цифру и специальный символ')


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Tcccc...', validators=[DataRequired(), Length(min=6), password_validator])
    confirm = PasswordField('Tcccc...[2]', validators=[DataRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Tcccc...', validators=[DataRequired()])






