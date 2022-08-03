from crypt import methods
from curses.ascii import US
from datetime import date
from bcrypt import re
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.employ import Employeed


@app.route('/employee_register', methods=['POST'])
def employee_register():
    if 'user_id' not in session:
        return redirect('/')
    if not Employeed.validate_register(request.form):
        return redirect('/dashboard')
    data = { 
        "id": session['user_id'],
        "account_id": request.form['account_id'],
        "position": request.form['position'],
    }


    employee = Employeed.save(data)
    session['employee_id'] = employee
    return redirect('/dashboard')