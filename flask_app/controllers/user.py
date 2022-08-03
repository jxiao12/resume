from curses.ascii import US
from datetime import date
from re import template
from bcrypt import re
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.employ import Employeed
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('homepage/index.html', drys=Product.get_type({'type':'dry'}), 
        freshs=Product.get_type({'type':'fresh'}), 
        frozzens=Product.get_type({'type':'frozzen'}))
    
    else:
        data = {
            'id': session['user_id']
        }
        return render_template('homepage/index.html', user=User.get_by_id(data),
        drys=Product.get_type({'type':'dry'}), 
        freshs=Product.get_type({'type':'fresh'}), 
        frozzens=Product.get_type({'type':'frozzen'}))


@app.route('/user_login')
def user_login():
    return render_template('user/login.html')


@app.route('/login',methods=['POST'])
def login():
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if EMAIL_REGEX.match(request.form['infor']):
        data = {
            'email': request.form['infor']
        }
        user = User.get_by_email(data)

    else:
        data = {
            'username': request.form['infor']
        }
        user = User.get_by_username(data)
    
    if not user:
        flash("Invalid Email or Username","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    
    return redirect('/dashboard')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = { 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "username": request.form['username'],
        "amount": 0,
        "password": bcrypt.generate_password_hash(request.form['password']),
        "employee_id":0,
    }

    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def show():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('user/show.html', user=User.get_by_id(data))


@app.route('/charged',methods=['POST'])
def money_charged():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
       'amount': request.form.get('charged', type=float) + request.form.get('balance', type=float),
       'id': session['user_id']
    }
    User.money_charged(data)
    return redirect('/dashboard')


@app.route('/employeeEnter')
def employee_enter():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    user = User.get_by_id(data)
    if len(Employeed.get_all_id(data)) == 1:
        user.is_employee = True
        user.employee_id = user.id
        session['employee_id'] = session['user_id']
    return render_template('user/employee.html', user=user)

@app.route('/cart')
def cart_show():
    if 'user_id' not in session:
        return redirect('/logout')

    return render_template('/user/cart.html', user=User.get_by_id({'id':session['user_id']}))

