from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import tree
from flask_app.models import user
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'arbortrary_schema';
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.tree = None
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
    		VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @staticmethod
    def validate_user_reg(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.DB).query_db(query,user)
        if len(user['first_name']) < 3 or len(user['last_name']) < 3:
            flash("Name should be at least 3 characters.", 'name_short')
            is_valid = False
        if any(str.isdigit(n) for n in user['first_name']) == True or any(str.isdigit(n) for n in user['last_name']) == True:
            flash("Name shouldn't contain any numbers.", 'name_no_num')
            is_valid = False
        if len(result) >= 1:
            flash("Email is already registered.", 'email_registered')
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", 'email_invalid')
            is_valid = False
        if len(user['password']) < 9:
            flash("Password needs to be at least 8 characters.", 'password_short')
            is_valid = False
        if user['password'] != user['confirm_password'] :
            flash("Passwords do not match.", 'passwords_no_match')
            return False
        return is_valid
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def add_to_visit_count(cls, data):
        query = """
        INSERT INTO page_visits (user_id, tree_id)
        VALUES (%(user_id)s, %(tree_id)s);
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    
    @classmethod
    def get_all_visitors_by_tree_id(cls, data):
        query = """
        SELECT * FROM users
        JOIN page_visits ON page_visits.user_id = users.id
        JOIN trees ON page_visits.tree_id = trees.id
        WHERE trees.id = %(tree_id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        # all_visitors = result
        all_visitors = []
        for row in result:
            visitor_info = cls(row)
            # print(visitor_info.id)
            tree_data = {
                "id" : row["trees.id"],
                "species" : row["species"],
                "location" : row["location"],
                "reason" : row["reason"],
                "date_planted" : row["date_planted"],
                "visit_count" : row["visit_count"],
                "created_at" : row['trees.created_at'],
                "updated_at" : row["trees.updated_at"]
            }
            visitor_info.tree = tree.Tree(tree_data)
            all_visitors.append(visitor_info)
        # print(all_visitors)
        return all_visitors
    

        