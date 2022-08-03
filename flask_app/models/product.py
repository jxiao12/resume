from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models.employ import Employeed

class Product:
    db_name = "mydb"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.best_by = data['best_by']
        self.cost = data['cost']
        self.quanlity = data['quanlity']
        self.create = data['create']
        self.upload = data['upload']
        self.employee_id = data['employee_id']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO product (name, type, best_by, cost, quanlity, employee_id) VALUES(%(name)s,%(type)s,%(best_by)s,%(cost)s, %(quanlity)s, %(employee_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM product;"
        results = connectToMySQL(cls.db_name).query_db(query)
        products = []
        for row in results:
            products.append( cls(row))
        return products

    @classmethod
    def get_type(cls, data):
        query = "SELECT * FROM product WHERE type = %(type)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        products = []
        for row in results:
            products.append( cls(row))
        return products


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM product WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_by_name(cls,data):
        query = "SELECT * FROM product WHERE name = %(name)s;"
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
    def update(cls, data):
        query = "UPDATE product SET name=%(name)s, type=%(type)s, cost=%(cost)s, best_by=%(best_by)s, quanlity=%(quanlity)s, upload=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_one_with_creator(cls, data):
        query = "SELECT * FROM employee LEFT JOIN product ON employee.id = product.employee_id WHERE product.id=%(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        one_show = cls(result[0])
        creator_info = {
            'id':result[0]['employee_id'],
            'account_id':result[0]['account_id'],
            'position':result[0]['position'],
            'create':result[0]['create'],
            'upload':result[0]['upload']
        }
        one_user = Employeed(creator_info)
        one_show.creator = one_user
        return one_show


    @staticmethod
    def update_check(user):
        is_valid = True
        query = "SELECT * FROM product WHERE name = %(name)s;"
        results = connectToMySQL(Product.db_name).query_db(query,user)
        from datetime import datetime

        today = datetime.now()
        date_string = datetime.fromisoformat(user['best_by'])
        
        if len(results) == 1:
            flash("Nothing, Please check again!.","register")
            is_valid=False
        if len(user['name']) < 2:
            flash("Product name must be at least 3 characters","register")
            is_valid= False
        
        if len(user['cost']) < 0:
            flash("The money is wrong!","register")
            is_valid= False

        if date_string < today:
            flash("The date is Wrong!","register")
            is_valid= False
        return is_valid