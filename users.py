from flask import render_template, session, redirect, request, flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User


bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)

    if not is_valid:
        return redirect("/")
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    id = User.save(new_user)
    if not id:
        flash("Email already taken.", "register")
        return redirect('/')
    session['user_id'] = id
    return redirect('/logged_in')


@app.route("/login", methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user = User.get_by_email(data)
    print("**********************************")
    print(user.password)
    if not user:
        flash("Invalid Email/Password", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect('/logged_in')


@app.route("/logged_in")
def logged_in():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_one(data)
    users = User.get_all()
    return render_template("logged_in.html", user=user, users=users)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
