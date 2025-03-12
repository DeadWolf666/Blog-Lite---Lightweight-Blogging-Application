from configuration.database import db
from flask_login import UserMixin
from sqlalchemy.sql import func

followers = db.Table('followers', db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

# User model with self-referential relationship to show followed users
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    doj = db.Column(db.DateTime(timezone=True), default=func.now())
    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(followers.c.followed_id == id), backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    posts = db.relationship('Blog', backref='user', passive_deletes=True)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

# Blog model referencing User model for authorship
class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    caption = db.Column(db.String)
    imageURL = db.Column(db.String)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
