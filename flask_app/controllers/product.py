from crypt import methods
from curses.ascii import US
from datetime import date
from turtle import pencolor
from bcrypt import re
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.employ import Employeed


@app.route('/new/thing')
def new_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if 'employee_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['employee_id']
    }

    return render_template('product/create.html',em=Employeed.get_by_id(data))

@app.route('/create/thing',methods=['POST'])
def create_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if 'employee_id' not in session:
        return redirect('/logout')
    if not Product.update_check(request.form):
        return redirect('/new/thing')
    data = {
        "name": request.form["name"],
        "type": request.form["type"],
        "best_by": request.form["best_by"],
        "cost": request.form["cost"],
        "quanlity": request.form["quanlity"],
        "employee_id": session["employee_id"]
    }
    product = Product.save(data)
    session['id'] = product
    return redirect('/dashboard')

@app.route('/destroy/<int:id>')
def destroy_product(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if 'employee_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Product.destroy(data)
    return redirect('/dashboard')


@app.route('/show/<int:id>')
def show_product(id):
    if 'employee_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['employee_id']
    }
    return render_template("product/showthing.html",product=Product.get_one_with_creator(data),user=Employeed.get_by_id(user_data))


@app.route('/edit/<int:id>')
def edit_product(id):
    if 'user_id' not in session:
        return redirect('/logout')

    if 'employee_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['employee_id']
    }
    return render_template("edit.html",edit=Product.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/product',methods=['POST'])
def update_sasquatch():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_recipe(request.form):
        return redirect('/new/sasquatch')
    data = {
        "name": request.form["name"],
        "type": request.form["type"],
        "best_by": request.form["best_by"],
        "cost": request.form["cost"],
        "quanlity": request.form["quanlity"],
        "employee_id": session["employee_id"]
    }
    Product.update(data)
    return redirect('/dashboard')

@app.route('/purchase/<int:id>')
def purchase(id):
    if 'user_id' not in session:
        return redirect('/logout')
    product = Product.get_by_id({'id':id})
    user = User.get_by_id({'id':session['user_id']})

    data = {
        "id":id,
        "name": product.name,
        "type": product.type,
        "best_by": product.best_by,
        "cost": product.cost,
        "quanlity": product.quanlity
    }
    if data['quanlity'] <= 0:
        return redirect('/dashboard')
    if user.amount < product.cost - 50:
        return redirect('/dashboard')
    
    user.money_charged({'id':user.id, 'amount':user.amount - product.cost})
    data['quanlity'] = data['quanlity'] - 1

    product.update(data)
    print(user.amount, product.quanlity)
    return redirect('/')

@app.route('/addcart/<int:id>')
def add_cart(id):
    if 'user_id' not in session:
        return redirect('/logout')

    product = Product.get_by_id({'id':id}).id
    user_id = User.get_by_id({'id':session['user_id']}).id
    User.add({'id':user_id}, {'id':product})

    return redirect('/')
