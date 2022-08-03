from flask_app.config.mysqlconnection import connectToMySQL
import re

from flask_app.models.product import Product

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db_name = "mydb"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.amount = data['amount']
        self.create = data['create']
        self.upload = data['upload']
        
        self.employee_id = 0
        self.is_employee = False
        self.cart = []


    @classmethod
    def save(cls, data):
        print(data)
        query = "INSERT INTO user (first_name, last_name, username, email, password, amount) VALUES(%(first_name)s,%(last_name)s,%(username)s,%(email)s,%(password)s, %(amount)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM user WHERE username = %(username)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])


    @classmethod
    def get_by_lastname(cls,data):
        query = "SELECT * FROM user WHERE last_name = %(last_name)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM user WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    
    @classmethod
    def get_by_firstname(cls,data):
        query = "SELECT * FROM user WHERE first_name = %(first_name)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        users = []
        for row in results:
            users.append( cls(row))
        return users


    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"

        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False

        query_username = "SELECT * FROM user WHERE username = %(username)s;"
        result_username = connectToMySQL(User.db_name).query_db(query_username,user)
        if len(result_username) >= 1:
            flash("Username already taken.","register")
            is_valid=False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters","register")
            is_valid= False

        if len(user['username']) < 2:
            flash("Username must be at least 3 characters","register")
            is_valid= False
        
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid


    @classmethod
    def money_charged(cls,data):
        query = "UPDATE user SET amount=%(amount)s where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    # @classmethod
    # def add(cls, data, product):
    #     query = "SELECT * FROM user WHERE id = %(id)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query,data)
    #     user = cls(results[0])

    #     user.cart = user.cart.append(Product.get_by_id(product))
    #     return user