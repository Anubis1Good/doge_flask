from flask import Flask, render_template, url_for, redirect,session,request
from dotenv import load_dotenv
from db.db_scripts import do
import os
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

DEBUG = os.getenv('DEBUG')
SECRET_KEY = os.getenv('SECRET_KEY')


app = Flask(__name__)
app.secret_key=SECRET_KEY
# hash = generate_password_hash('1234')
# print(hash)

@app.route('/')
def index():
    if 'name' in session:
        return render_template('index.html',title='Главная', name=session['name'])
    return render_template('index.html',title='Главная')

@app.route('/users')
def users():
    if 'name' in session:
        data = do('SELECT * FROM Users')
        return render_template('users.html', title='Все пользователи', users=data, name=session['name'])
    return redirect(url_for('login'))

@app.route('/user/<username>')
def user(username):
    return render_template('user.html',title=username, name=username)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password =request.form['password']
        data = do(f'SELECT * FROM Login WHERE login="{name}"')
        if not data:
            return render_template('login.html',title='Вход',error='login')
        else:
            is_ok = check_password_hash(data[0][2],password)
            if is_ok:
                data = do(f'SELECT name FROM Users WHERE id={data[0][3]}')
                session['name'] = data[0][0]
                return redirect(url_for('user',username=session['name']))
            return render_template('login.html',title='Вход',error='password')
    return render_template('login.html',title='Вход')
    

@app.route('/exit')
def exit():
    session.clear()
    return redirect(url_for('index'))

@app.route('/registration',methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        
        return render_template('registration.html',title='Регистрация')
    return render_template('registration.html',title='Регистрация')

app.run(debug=DEBUG)
