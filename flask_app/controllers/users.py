from flask_app import app, bcrypt
from flask import redirect, render_template, request, session, flash
from flask_app.models.user import User


@app.get("/")
def index():
    return render_template("index.html")

@app.post("/users/register")
def register():
    if not User.register_form_is_valid(request.form):
        return redirect("/")
    
    potential_user = User.find_by_email(request.form["email"])

    if potential_user != None:
        print(request.form)
        flash("Email is in use. Please login", "register")
        return redirect("/")
    
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw,
    }
    user_id = User.register(user_data)
    session["user_id"] = user_id
    return redirect("/products/all")

    
@app.post("/users/login")
def login():
    if not User.login_form_is_valid(request.form):
        return redirect("/")
    
    potential_user = User.find_by_email(request.form['email'])
    if potential_user == None:
        flash("Invalid credentials.", "login")
        return redirect("/")
    
    user = potential_user
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid credentials.", "login")
        return redirect("/")
    
    session['user_id'] = user.id
    return redirect("/products/all")

@app.get("/users/logout")
def logout():
    session.clear()
    return redirect("/")