# from flask_app import app
# from flask import render_template, session, flash, redirect, request
# from flask_app.models.product import Movie
# from flask_app.models.user import User
# import requests

# TMDB_API_KEY = '2d6086ca254b8621b38e157701ad43ff'

# @app.get("/movies/all")
# def all_movies():

#     if "user_id" not in session:
#         flash("You must be logged in to view that page", "login")
#         return redirect("/")

#     movies = Movie.find_all_with_users()
#     user = User.find_by_user_id(session["user_id"])
#     return render_template("all_movies.html", movies=movies, user=user)

# @app.get("/movies/new")
# def new_movie():

#     if "user_id" not in session:
#         flash("You must be logged in to view that page", "login")
#         return redirect("/")
    
#     user = User.find_by_user_id(session["user_id"])
#     return render_template("new_movie.html", user=user)

# @app.post("/movies/create")
# def create_movie():

#     if "user_id" not in session:
#         flash("You must be logged in to view that page", "login")
#         return redirect("/")

#     if not Movie.form_is_valid(request.form):
#         return redirect("/movies/new")
    
#     title = request.form.get('title')
#     tmdb_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
#     response = requests.get(tmdb_url)
#     movie_data = response.json()
#     print(movie_data)
#     if movie_data['results']:
#         poster_path = movie_data['results'][0].get('poster_path', '')
#         poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
#     else:
#         poster_url = ''

#     form_data = {
#         'title': request.form['title'],
#         'director': request.form['director'],
#         'release_date': request.form['release_date'],
#         'score': request.form['score'],
#         'user_id': session['user_id'],
#         'poster_url': poster_url
#     }
    
#     Movie.create(form_data)
#     return redirect("/movies/all")

# @app.get("/movies/<int:movie_id>")
# def show_movie(movie_id):

#     if "user_id" not in session:
#         flash("You must be logged in to view that page", "login")
#         return redirect("/")

#     movie = Movie.find_by_id_with_user(movie_id)
#     user = User.find_by_user_id(session["user_id"])

#     return render_template("show_movie.html", movie=movie, user=user)

# @app.get("/movies/<int:movie_id>/edit")
# def edit_movie(movie_id):

#     if "user_id" not in session:
#         flash("You must be logged in to view that page", "login")
#         return redirect("/")
    
#     movie = Movie.find_by_id_with_user(movie_id)

#     if movie is None:
#         flash('Movie not found.')
#         return redirect('/movies/all')
    
#     if movie.user.id != session['user_id']:
#         flash('You do not have permission to edit this movie')
#         return redirect('/movies/all')
    
#     user = User.find_by_user_id(session["user_id"])
#     return render_template("edit_movie.html", movie=movie, user=user)

# @app.post("/movies/<int:movie_id>/update")
# def update_movie(movie_id):

#     if "user_id" not in session:
#         flash("You must be logged in to view that page", "login")
#         return redirect("/")
    
#     movie_id = request.form['movie_id']
#     movie = Movie.find_by_id_with_user(movie_id)

#     if movie is None:
#         flash('Movie not found.')
#         return redirect('/movies/all')
    
#     if movie.user.id != session['user_id']:
#         flash('You do not have permission to edit this movie')
#         return redirect('/movies/all')
    
#     if not Movie.form_is_valid(request.form):
#         return redirect(f"/movies/{movie_id}/edit")
    
#     Movie.update(request.form)
#     return redirect('/movies/all')

# @app.post("/movies/<movie_id>/delete")
# def delete_movie(movie_id):

#     if "user_id" not in session:
#         flash("You must be logged in to view that page", "login")
#         return redirect("/")

#     Movie.delete(movie_id)
#     return redirect("/movies/all")

from flask_app import app
from flask import render_template, session, flash, redirect, request
from flask_app.models.product import Product
from flask_app.models.user import User
import requests

@app.get("/products/all")
def all_products():

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")

    products = Product.find_all_with_users()
    user = User.find_by_user_id(session["user_id"])
    return render_template("all_products.html", products=products, user=user)

@app.get("/products/new")
def new_product():

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    user = User.find_by_user_id(session["user_id"])
    return render_template("new_product.html", user=user)

@app.post("/products/create")
def create_product():

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")

    if not Product.form_is_valid(request.form):
        return redirect("/products/new")
    
    # Example: Getting product data from FakestoreAPI
    product_id = request.form.get('product_id')
    fakestore_url = f"https://fakestoreapi.com/products/{product_id}"
    response = requests.get(fakestore_url)
    product_data = response.json()

    form_data = {
        'title': product_data['title'],
        'price': product_data['price'],
        'description': product_data['description'],
        'category': product_data['category'],
        'user_id': session['user_id'],
        'image_url': product_data.get('image', ''),
        'rating': product_data.get('rating', {}).get('rate', 0)
    }
    
    Product.create(form_data)
    return redirect("/products/all")

@app.get("/products/<int:product_id>")
def show_product(product_id):

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")

    product = Product.find_by_id_with_user(product_id)
    user = User.find_by_user_id(session["user_id"])

    return render_template("show_product.html", product=product, user=user)

@app.get("/products/<int:product_id>/edit")
def edit_product(product_id):

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    product = Product.find_by_id_with_user(product_id)

    if product is None:
        flash('Product not found.')
        return redirect('/products/all')
    
    if product.user.id != session['user_id']:
        flash('You do not have permission to edit this product')
        return redirect('/products/all')
    
    user = User.find_by_user_id(session["user_id"])
    return render_template("edit_product.html", product=product, user=user)

@app.post("/products/<int:product_id>/update")
def update_product(product_id):

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    product_id = request.form['product_id']
    product = Product.find_by_id_with_user(product_id)

    if product is None:
        flash('Product not found.')
        return redirect('/products/all')
    
    if product.user.id != session['user_id']:
        flash('You do not have permission to edit this product')
        return redirect('/products/all')
    
    if not Product.form_is_valid(request.form):
        return redirect(f"/products/{product_id}/edit")
    
    Product.update(request.form)
    return redirect('/products/all')

@app.post("/products/<product_id>/delete")
def delete_product(product_id):

    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")

    Product.delete(product_id)
    return redirect("/products/all")


