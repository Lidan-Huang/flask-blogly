"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = '/static/tree.jpeg'
#can clean up default image url

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class USER(db.Model):
    """User docstrings"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.Text, default=DEFAULT_IMAGE_URL, nullable = False)


class Post(db.Model):
    """Post docstrings"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # users = db.relationship('Post', backref="users")