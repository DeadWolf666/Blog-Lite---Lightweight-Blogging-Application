from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from configuration.database import db
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

# Log in
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password!", category='error')
        else:
            flash("Email not registered!", category='error')

    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for("views.home"))
    
    return render_template("login.html", logged_user=current_user)

# Sign up
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        user_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("Email already in use!", category='error')
        elif user_exists:
            flash("Username has been taken!", category='error')
        elif len(username) > 10:
            flash("Username cannot be more than 10 characters long!", category='error')
        elif len(password1) < 8:
            flash("Password is too short!", category='error')
        elif password1 != password2:
            flash("Password entered incorrectly!", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Created account!", category='info')
            return redirect(url_for("views.home"))
    
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for("views.home"))

    return render_template("signup.html", logged_user=current_user)

# Log out
@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
