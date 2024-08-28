from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app.models.user import User
from flask import flash
import re
from datetime import date



class Movie:
    _db = "movie_db"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.director = data["director"]
        self.release_date = data["release_date"]
        self.score = data["score"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users_id = data["users_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):

        is_valid = True

        if len(form_data['title'].strip()) == 0:
            flash("Please enter title")
            is_valid = False
        elif len(form_data['title'].strip()) < 2:
            flash("Title must be at least 2 characters")
            is_valid = False

        if len(form_data['director'].strip()) == 0:
            flash("Please enter director")
            is_valid = False
        elif len(form_data['director'].strip()) < 5:
            flash("Director must be at least 5 characters")
            is_valid = False

        if len(form_data['release_date'].strip()) == 0:
            flash("Please enter date")
            is_valid = False
        elif form_data['release_date'] > date.today().isoformat():
            flash("Date cannot be in the future.")
            is_valid = False
        
        score_pattern = re.compile(r'^[1-9]$|^10$')
        if not score_pattern.match(form_data['score']):
            flash("Score must be a number between 1 and 10.")
            is_valid = False


        return is_valid


    @classmethod
    def find_all(cls):

        query = "SELECT * FROM movies;"
        list_of_dicts = connect_to_mysql(Movie._db).query_db(query)
        movies = []

        for each_dict in list_of_dicts:
            movie = Movie(each_dict)
            movies.append(movie)

        return movies
    
    @classmethod
    def find_all_with_users(cls):

        query = """
        SELECT * FROM movies
        JOIN users
        ON movies.users_id = users.id;
        """
        list_of_dicts = connect_to_mysql(Movie._db).query_db(query)
        movies = []

        for each_dict in list_of_dicts:
            movie = Movie(each_dict)
            user_data = {
                "id": each_dict["id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["created_at"],
                "updated_at": each_dict["updated_at"],
            }
            user = User(user_data)
            movie.user = user
            movies.append(movie)

        return movies
    
    @classmethod
    def create(cls, form_data):

        query = """
        INSERT INTO movies
        (title, director,  release_date, score, users_id)
        VALUES
        (%(title)s, %(director)s, %(release_date)s, %(score)s, %(user_id)s);
        """

        print(form_data)
        movie_id = connect_to_mysql(Movie._db).query_db(query, form_data)
        return movie_id
    
    @classmethod
    def find_by_id_with_user(cls, movie_id):

        query ="""
        SELECT * FROM movies
        JOIN users
        ON movies.users_id = users.id
        WHERE movies.id = %(movie_id)s;
        """
        data = {"movie_id": movie_id}
        list_of_dicts = connect_to_mysql(Movie._db).query_db(query, data)
        movie = Movie(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]['users.id'],
            "first_name": list_of_dicts[0]['first_name'],
            "last_name": list_of_dicts[0]['last_name'],
            "email": list_of_dicts[0]['email'],
            "password": list_of_dicts[0]['password'],
            "created_at": list_of_dicts[0]['users.created_at'],
            "updated_at": list_of_dicts[0]['users.updated_at'],
        }

        user = User(user_data)
        movie.user = user
        return movie
    
    @classmethod
    def update(cls, form_data):

        query = """
        UPDATE movies
        SET
        title = %(title)s,
        director = %(director)s,
        release_date = %(release_date)s,
        score = %(score)s
        WHERE id = %(movie_id)s;
        """

        connect_to_mysql(Movie._db).query_db(query, form_data)
        return
    
    @classmethod
    def delete(cls, movie_id):

        query = """
        DELETE FROM movies
        WHERE id = %(movie_id)s;
        """
        data = {"movie_id": movie_id}
        connect_to_mysql(Movie._db).query_db(query, data)
        return



