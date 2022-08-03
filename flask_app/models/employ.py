from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Employeed:
    db_name = "mydb"

    def __init__(self, data):
        self.id = data['id']
        self.account_id = data['account_id']
        self.position = data['position']
        self.create = data['create']
        self.upload = data['upload']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO employee (id, account_id, position) VALUES(%(id)s, %(account_id)s,%(position)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM employee;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM employee WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_id(cls, data):
        query = "SELECT * FROM employee WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_position(cls,data):
        query = "SELECT * FROM employee WHERE position = %(position)s;"
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
        query = "UPDATE employee SET account_id=%(account_id)s, position=%(position)s, upload=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_register(employee):
        is_valid = True
        query = "SELECT * FROM employee WHERE account_id = %(account_id)s;"
        results = connectToMySQL(Employeed.db_name).query_db(query,employee)
        if len(results) >= 1:
            flash("ID already taken.","register")
            is_valid=False
        
        if len(employee['position']) < 2:
            flash("Position must be at least 3 characters","register")


        return is_valid