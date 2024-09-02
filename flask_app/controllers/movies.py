from flask_app import app
from flask import render_template, session, flash, redirect, request
from flask_app.models.movie import Movie
from flask_app.models.user import User
import requests

TMDB_API_KEY = '2d6086ca254b8621b38e157701ad43ff'

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
    
    title = request.form.get('title')
    tmdb_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(tmdb_url)
    movie_data = response.json()
    print(movie_data)
    if movie_data['results']:
        poster_path = movie_data['results'][0].get('poster_path', '')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
    else:
        poster_url = ''

    form_data = {
        'title': request.form['title'],
        'director': request.form['director'],
        'release_date': request.form['release_date'],
        'score': request.form['score'],
        'user_id': session['user_id'],
        'poster_url': poster_url
    }
    
    Movie.create(form_data)
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

@app.post("/movies/<int:movie_id>/update")
def update_movie(movie_id):

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

