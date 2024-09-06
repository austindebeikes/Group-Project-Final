from flask_app import app
from flask import render_template, session, flash, redirect, request
from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app.models.product import Product
from flask_app.models.user import User
import requests

@app.get("/products/all")
def all_products():
    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    user_id = session['user_id']
    products = response.json()
    
    user = User.find_by_user_id(session["user_id"])
    return render_template("all_products.html", products=products, user=user, user_id=user_id)

@app.get("/products/<int:product_id>/edit")
def edit_product(product_id):
    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    url = f"https://fakestoreapi.com/products/{product_id}"
    response = requests.get(url)
    product = response.json()
    
    user = User.find_by_user_id(session["user_id"])
    return render_template("edit_product.html", product=product, user=user)

@app.post("/products/<int:product_id>/update")
def update_product(product_id):
    if "user_id" not in session:
        flash("You must be logged in to perform that action", "login")
        return redirect("/")
    
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "rating": request.form["rating"],
        "category": request.form["category"]
    }

    url = f"https://fakestoreapi.com/products/{product_id}"
    response = requests.put(url, json=data)
    
    if response.ok:
        flash("Product updated successfully", "success")
        return redirect(f"/products/{product_id}")
    else:
        flash("Failed to update product", "error")
        return redirect(f"/products/{product_id}/edit")

@app.post("/products/<int:product_id>/delete")
def delete_product(product_id):
    if "user_id" not in session:
        flash("You must be logged in to perform that action", "login")
        return redirect("/")
    
    url = f"https://fakestoreapi.com/products/{product_id}"
    response = requests.delete(url)
    
    if response.ok:
        flash("Product deleted successfully", "success")
        return redirect("/products/all")
    else:
        flash("Failed to delete product", "error")
        return redirect(f"/products/{product_id}")

@app.get("/products/<int:product_id>")
def show_product(product_id):
    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    url = f"https://fakestoreapi.com/products/{product_id}"
    response = requests.get(url)
    product = response.json()
    
    user = User.find_by_user_id(session["user_id"])
    return render_template("show_product.html", product=product, user=user)

@app.get("/products/add")
def add_product():
    if "user_id" not in session:
        flash("You must be logged in to view that page", "login")
        return redirect("/")
    
    user = User.find_by_user_id(session["user_id"])
    return render_template("new_product.html", user=user)

@app.post("/products/create")
def create_product():
    if "user_id" not in session:
        flash("You must be logged in to perform that action", "login")
        return redirect("/")
    
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "rating": request.form["rating"],
        "category": request.form["category"]
    }

    url = "https://fakestoreapi.com/products"
    response = requests.post(url, json=data)
    
    if response.ok:
        flash("Product added successfully", "success")
        return redirect("/products/all")
    else:
        flash("Failed to add product", "error")
        return redirect("/products/add")
    
@app.route('/products/<int:product_id>/favorite', methods=['POST'])
def favorite_product(product_id):
    if 'user_id' not in session:
        flash("You must be logged in to perform that action", "login")
        return redirect('/')

    user_id = session['user_id']
    
    # Fetch product data from the API
    product_data = requests.get(f'https://fakestoreapi.com/products/{product_id}').json()

    # Check if product already exists in the database
    existing_product = Product.find_by_id(product_id)
    if not existing_product:
        # If it doesn't exist, add it to the database
        form_data = {
            "title": product_data['title'],
            "price": product_data['price'],
            "description": product_data['description'],
            "category": product_data['category'],
            "image_url": product_data['image'],
            "rating": product_data['rating']['rate'],
            "user_id": user_id
        }
        Product.create(form_data)
    else:
        # If the product exists, update the user_id to link it with the current user
        query = "UPDATE products SET user_id = %s WHERE id = %s"
        connect_to_mysql(Product._db).query_db(query, (user_id, product_id))
    
    flash(f"{product_data['title']} has been added to your list!", "success")
    return redirect('/products/all')

@app.route('/users/<int:user_id>/products', methods=['GET'])
def user_products(user_id):
    if 'user_id' not in session:
        flash("You must be logged in to view that page", "login")
        return redirect('/')

    if user_id != session['user_id']:
        flash("You do not have permission to view these products", "error")
        return redirect('/')

    # Fetch the user's products
    query = "SELECT * FROM products WHERE user_id = %s"
    products = connect_to_mysql(Product._db).query_db(query, (user_id,))
    
    return render_template("user_products.html", products=products, user_id=user_id)

@app.route('/products/<int:product_id>/remove', methods=['POST'])
def remove_product(product_id):
    if 'user_id' not in session:
        flash("You must be logged in to perform that action", "login")
        return redirect('/')

    user_id = session['user_id']

    # Remove the product from the user's list
    query = "DELETE FROM products WHERE id = %s AND user_id = %s"
    result = connect_to_mysql(Product._db).query_db(query, (product_id, user_id))

    if result:
        flash("Product removed successfully!", "success")

    return redirect(f'/users/{user_id}/products')
