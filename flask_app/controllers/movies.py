from flask_app import app
from flask import render_template, session, flash, redirect, request
from flask_app.models.movie import Movie
from flask_app.models.user import User

@app.get("/movies/all")
def all_movies():

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")

    movies = Movie.find_all_with_users()
    user = User.find_by_user_id(session["user_id"])
    return render_template("all_movies.html", movies=movies, user=user)

@app.get("/movies/new")
def new_movie():

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    user = User.find_by_user_id(session["user_id"])
    return render_template("new_movie.html", user=user)

@app.post("/movies/create")
def create_movie():

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")

    if not Movie.form_is_valid(request.form):
        return redirect("/movies/new")
    
    Movie.create(request.form)
    return redirect("/movies/all")

@app.get("/movies/<int:movie_id>")
def show_movie(movie_id):

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")

    movie = Movie.find_by_id_with_user(movie_id)
    user = User.find_by_user_id(session["user_id"])

    return render_template("show_movie.html", movie=movie, user=user)

@app.get("/movies/<int:movie_id>/edit")
def edit_movie(movie_id):

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    movie = Movie.find_by_id_with_user(movie_id)

    if movie is None:
        flash('Movie not found.')
        return redirect('/movies/all')
    
    if movie.user.id != session['user_id']:
        flash('You do not have permission to edit this movie')
        return redirect('/movies/all')
    
    user = User.find_by_user_id(session["user_id"])
    return render_template("edit_movie.html", movie=movie, user=user)

@app.post("/movies/update")
def update_movie():

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    movie_id = request.form['movie_id']
    movie = Movie.find_by_id_with_user(movie_id)

    if movie is None:
        flash('Movie not found.')
        return redirect('/movies/all')
    
    if movie.user.id != session['user_id']:
        flash('You do not have permission to edit this movie')
        return redirect('/movies/all')
    
    if not Movie.form_is_valid(request.form):
        return redirect(f"/movies/{movie_id}/edit")
    
    Movie.update(request.form)
    return redirect('/movies/all')

@app.post("/movies/<movie_id>/delete")
def delete_movie(movie_id):

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")

    Movie.delete(movie_id)
    return redirect("/movies/all")

