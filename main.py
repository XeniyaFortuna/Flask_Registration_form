from flask import Flask, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import escape
from flask_wtf.csrf import CSRFProtect
from models import db, User
from forms import RegisterForm, LoginForm
from secrets import token_bytes
from time import sleep

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = token_bytes()
db.init_app(app)
csrf = CSRFProtect()




@app.cli.command('init-db')
def init_db():
    db.create_all()
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.get('/register/')
def register_get():
    form = RegisterForm()
    return render_template('register.html', form=form)



@app.post('/register/')
def register_post():
    form = RegisterForm()
    if form.validate():
        username = escape(form.username.data)
        email = escape(form.email.data)
        password = escape(generate_password_hash(form.password.data))
        check_username = User.query.filter_by(username=username).first()
        check_email = User.query.filter_by(email=email).first()

        if check_username != None:
            flash('Пользователь с таким именем уже существует', 'warning')
            return render_template('register.html', form=form)
        if check_email != None:
            flash('Пользователь с такой почтой уже существует', 'warning')
            return render_template('register.html', form=form)

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    flash('Регистрация не выполнена', 'warning')
    return render_template('register.html', form=form)



@app.get('/login/')
def login_get():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.post('/login/')
def login_post():
    form = LoginForm()
    email = escape(form.email.data)
    password = escape(form.password.data)
    user = User.query.filter_by(email=email).first()
    if user:
        check_password = check_password_hash(user.password, password)
        if check_password:
            return redirect(url_for('index'))
        else:
            flash('пароль неверный', 'warning')
            return render_template('login.html', form=form)
    else:
        flash('пользователь с таким email не зарегистрирован', 'warning')
        return render_template('login.html', form=form)


# Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
# содержать следующие поля:
# ○ Имя пользователя (обязательное поле)
# ○ Электронная почта (обязательное поле, с валидацией на корректность ввода email)
# ○ Пароль (обязательное поле, с валидацией на минимальную длину пароля)
# ○ Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
# После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
# и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
# заполнено или данные не прошли валидацию, то должно выводиться соответствующее
# сообщение об ошибке.
# Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
# базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
# об ошибке.


if __name__ == '__main__':
    app.run(debug=True)