from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Tree:
    DB = 'arbortrary_schema';
    def __init__( self , data ):
        self.id = data['id']
        # self.user_id = data['user_id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date_planted = data['date_planted']
        self.visit_count = data['visit_count']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls, data):
        query = """INSERT INTO trees (species, location, reason, date_planted, user_id)
    		VALUES (%(species)s, %(location)s, %(reason)s, %(date_planted)s, %(user_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        # print(result)
        return result
    
    @classmethod
    def get_all_trees(cls):
        query = """SELECT * FROM trees 
                    LEFT JOIN users ON users.id = trees.user_id;"""
        result = connectToMySQL(cls.DB).query_db(query)
        all_trees = []
        for row in result:
            tree = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            tree.user = user.User(user_data)
            # print(tree, tree.user)
            all_trees.append(tree)
        # print(all_trees)
        return all_trees 
    
    @classmethod
    def get_all_trees_and_visits(cls):
        query = """SELECT * FROM trees 
                    LEFT JOIN users ON users.id = trees.user_id;"""
        result = connectToMySQL(cls.DB).query_db(query)
        all_trees = []
        for row in result:
            tree = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            tree.user = user.User(user_data)
            # print(tree, tree.user)
            all_trees.append(tree)
        # print(all_trees)
        return all_trees
    
    @classmethod
    def get_all_trees_by_user_id(cls, data):
        query = """
        SELECT * FROM trees 
        LEFT JOIN users ON users.id = trees.user_id
        WHERE users.id = %(user_id)s;"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        all_trees = []
        for row in result:
            tree = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            tree.user = user.User(user_data)
            # print(tree, tree.user)
            all_trees.append(tree)
        # print(all_trees)
        return all_trees 
    
    @classmethod
    def get_tree_by_id(cls, data):
        query = "SELECT * FROM trees LEFT JOIN users ON users.id = trees.user_id WHERE trees.id = %(tree_id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        tree_by_id = cls(result[0])
        # print(tree_by_id)
        # print(result[0])
        user_data = {
            "id" : result[0]["user_id"],
            "first_name" : result[0]["first_name"],
            "last_name" : result[0]["last_name"],
            "email" : result[0]["email"],
            "password" : result[0]["password"],
            "created_at" : result[0]["users.created_at"],
            "updated_at" : result[0]["users.updated_at"]
        }
        # print(user_data)
        tree_by_id.user = user.User(user_data)
        return tree_by_id
    
    @classmethod
    def update_tree(cls, data):
        query = """UPDATE trees 
                    SET species = %(species)s, location = %(location)s, reason = %(reason)s, date_planted = %(date_planted)s 
                    WHERE trees.user_id = %(user_id)s and trees.id = %(tree_id)s;""" #shouldnt need to check for both
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def delete_tree(cls, data):
        query = "DELETE FROM trees WHERE id = %(tree_id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @staticmethod
    def validate_tree(tree):
        is_valid = True
        if len(tree['species']) == 0 or len(tree['location']) == 0 or len(tree['reason']) == 0:
            flash("Fields must not be blank.", 'field_blank')
            is_valid = False
        if len(tree['species']) < 5:
            flash("Species must be at least 5 characters.", 'species_short')
            is_valid = False
        if len(tree['species']) < 2:
            flash("Location must be at least 2 characters.", 'location_short')
            is_valid = False
        if len(tree['species']) > 50:
            flash("Reason must be under 50 characters.", 'reason_long')
            is_valid = False
        return is_valid
    
    @classmethod
    def update_tree_visit_count(cls, data):
        query = """
        UPDATE trees
        SET trees.visit_count = (SELECT COUNT(page_visits.tree_id) FROM page_visits WHERE page_visits.tree_id = %(tree_id)s)
        WHERE trees.id = %(tree_id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
