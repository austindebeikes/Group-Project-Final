from flask_app.config.mysqlconnection import connect_to_mysql
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    _db = "movie_db"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def register_form_is_valid(form_data):
        is_valid = True

        if len(form_data['first_name'].strip()) == 0:
            flash("Please enter first name.", "register")
            is_valid = False
        elif len(form_data['first_name'].strip()) < 2:
            flash("First name must be at least 2 charcters.", "register")
            is_valid = False

        if len(form_data['last_name'].strip()) == 0:
            flash("Please enter last name.", "register")
            is_valid = False
        elif len(form_data['last_name'].strip()) < 2:
            flash("Last name must be at least 2 charcters.", "register")
            is_valid = False

        if len(form_data['email'].strip()) == 0:
            flash("Please enter email.", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Email address invalid.", "register")
            is_valid = False

        if len(form_data['password'].strip()) == 0:
            flash("Please enter password.", "register")
            is_valid = False
        elif len(form_data['password'].strip()) < 8:
            flash("Password must be at least 8 charcters.", "register")
            is_valid = False
        elif form_data["password"] != form_data["confirm_password"]:
            flash("Passwords do not match", "register")
            is_valid = False
        
        return is_valid
    
    @staticmethod
    def login_form_is_valid(form_data):
        is_valid = True

        if len(form_data['email'].strip()) == 0:
            flash("Please enter email.", "login")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Email address invalid.", "login")
            is_valid = False

        if len(form_data['password'].strip()) == 0:
            flash("Please enter password.", "login")
            is_valid = False
        elif len(form_data['password'].strip()) < 8:
            flash("Password must be at least 8 charcters.", "login")
            is_valid = False
        
        return is_valid
    
    @classmethod
    def register(cls, user_data):

        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """

        user_id = connect_to_mysql(User._db).query_db(query, user_data)
        return user_id
    
    @classmethod
    def find_by_email(cls, email):

        query = """SELECT * FROM users WHERE email = %(email)s"""
        data = {"email": email}
        list_of_dicts = connect_to_mysql(User._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user
    
    @classmethod
    def find_by_user_id(cls, user_id):

        query = """SELECT * FROM users WHERE id = %(user_id)s"""
        data = {"user_id": user_id}
        list_of_dicts = connect_to_mysql(User._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user