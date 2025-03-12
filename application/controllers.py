from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Blog, User, followers
from configuration.database import db
from sqlalchemy.sql import func
import os

controllers = Blueprint("controllers", __name__)

# Main dashboard page
@controllers.route("/", methods=["GET", "POST"])
@controllers.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    blogs = Blog.query.filter_by(author=current_user.id).order_by(Blog.timestamp)
    follower_list = User.query.join(followers, (followers.c.follower_id == User.id)).filter(followers.c.followed_id == current_user.id).all()
    return render_template("dashboard.html", logged_user=current_user, posts=blogs, followers=follower_list)

# User feed page
@controllers.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    followed_blogs = Blog.query.join(followers, (followers.c.followed_id == Blog.author)).filter(followers.c.follower_id == current_user.id).order_by(Blog.timestamp.desc())
    current_date = func.now()
    return render_template("feed.html", logged_user=current_user, display_posts=followed_blogs, date_now=current_date)

# Create a new blog
@controllers.route("/create", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "POST":

        title = request.form.get("title")
        caption = request.form.get("caption")
        file = request.files["image"]

        if not title:
            flash("Post must have a title!", category='error')
        elif not caption:
            flash("Post cannot be empty!", category='error')
        else:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                blog = Blog(title=title, caption=caption, author=current_user.id, imageURL=os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            else:
                blog = Blog(title=title, caption=caption, author=current_user.id, imageURL=None)
            db.session.add(blog)
            db.session.commit()
            flash("Post created!", category='success')
            return redirect(url_for(".dashboard"))

    return render_template("post.html", logged_user=current_user, blog=None)

# Edit an existing blog
@controllers.route("/edit/<blog_id>", methods=["GET", "POST"])
@login_required
def edit(blog_id):
    edit_blog = Blog.query.filter_by(id=blog_id).first()

    if request.method == "POST":

        title = request.form.get("title")
        caption = request.form.get("caption")
        image = request.files["image"]
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            edit_blog.imageURL = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        edit_blog.title = title
        edit_blog.caption = caption
        db.session.commit()
        return redirect(url_for(".dashboard"))

    return render_template("post.html", logged_user=current_user, blog=edit_blog)

# Delete an existing blog
@controllers.route("/delete/<blog_id>", methods=["GET", "POST"])
@login_required
def delete(blog_id):
    delete_blog = Blog.query.filter_by(id=blog_id).first()

    if request.method == "POST":
        db.session.delete(delete_blog)
        db.session.commit()
        flash("Blog deleted!", category='success')
        return redirect(url_for(".dashboard"))
    
    return render_template("delete.html", logged_user=current_user, blog=delete_blog)

# Search for users
@controllers.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":

        name = request.form.get("name")

        if not name:
            flash("Input a username to search!", category='error')
        else:
            user_exists = User.query.filter(User.username.like('%'+name+'%')).all()
            if not user_exists:
                flash("No user found!", category='message')
                return redirect(url_for(".search"))
            else:
                return render_template("search.html", logged_user=current_user, searched_user=user_exists)

    return render_template("search.html", logged_user=current_user, searched_user=None)

# View another user
@controllers.route("/<name>", methods=["GET", "POST"])
def userpage(name):
    userreq = User.query.filter_by(username=name).first()
    userblogs = Blog.query.filter_by(author=userreq.id).order_by(Blog.timestamp)
    follower_list = User.query.join(followers, (followers.c.follower_id == User.id)).filter(followers.c.followed_id == userreq.id).all()

    if current_user.is_authenticated:
        if userreq.id == current_user.id:
            return redirect(url_for(".dashboard"))
        if request.method == "POST":
            if not current_user.is_following(userreq):
                current_user.follow(userreq)
                db.session.commit()
            else:
                current_user.unfollow(userreq)
                db.session.commit()
            return redirect(url_for(".userpage", name=userreq.username))
    else:
        if request.method == "POST":
            flash("You must log in to follow other users!", category='error')
            return redirect(url_for("auth.login"))

    return render_template("dashboard.html", logged_user=current_user, posts=userblogs, display_user=userreq, followers=follower_list)

# View followers
@controllers.route("/<name>/followers", methods=["GET"])
def followers_display(name):
    userreq = User.query.filter_by(username=name).first()
    follower_list = User.query.join(followers, (followers.c.follower_id == User.id)).filter(followers.c.followed_id == userreq.id).all()
    return render_template("followers.html", logged_user=current_user, display_user=userreq, followers=follower_list)

# View followed
@controllers.route("/<name>/followed", methods=["GET"])
def followed_display(name):
    userreq = User.query.filter_by(username=name).first()
    followed_list = userreq.followed
    return render_template("followed.html", logged_user=current_user, display_user=userreq, followed=followed_list)

# View blogs
@controllers.route("/<name>/blogs", methods=["GET"])
def posts_display(name):
    userreq = User.query.filter_by(username=name).first()
    blogs = userreq.posts
    return render_template("posts.html", logged_user=current_user, display_user=userreq, posts=blogs)
