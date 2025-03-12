from flask import Blueprint, render_template
from flask_login import current_user
from application.models import Blog, User

views = Blueprint("views", __name__)

# Home view
@views.route("/", methods=["GET"])
@views.route("/home", methods=["GET"])
def home():
    return render_template("base.html", logged_user=current_user)

# Discover view
@views.route("/discover", methods=["GET"])
def discover():
    blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
    return render_template("discover.html", logged_user=current_user, posts=blogs)

# Display single post
@views.route("/<blog_id>", methods=["GET"])
def display(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    author = User.query.filter_by(id=blog.author).first()
    return render_template("display_post.html", logged_user=current_user, post=blog, writer=author)
