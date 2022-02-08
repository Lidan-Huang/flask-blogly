"""Blogly application."""

from flask import Flask, request, redirect, render_template, session
from models import db, connect_db, USER, DEFAULT_IMAGE_URL, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# USER ROUTES

@app.get('/')
def landing_page():
    """Shows home page"""

    return redirect('/users')

@app.get('/users')
def main_page():
    """Shows home page"""

    users = USER.query.all()
    return render_template('main-page.html', users=users)

@app.get('/users/new')
def show_new_user_form():
    """Shows new user input form"""

    return render_template('new-user.html')

@app.post('/users/new')
def add_new_user():
    """Retrieves from data and redirects user to users page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    image_url = image_url if image_url != "" else DEFAULT_IMAGE_URL

    user = USER(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show user detail page according to user_id from database"""

    user = USER.query.get_or_404(user_id)
    posts = Post.query.all()

    return render_template(
        "user-detail.html",
        user = user,
        posts = posts
    )

@app.get('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    """Show user edit page if they click cancel, redirect to user detail page
    if they click save, then we update the database"""
    
    user = USER.query.get_or_404(user_id)
    return render_template("user-edit.html", user = user)

@app.post('/users/<int:user_id>/edit')
def update_user_info(user_id):
    """Update user info button upon save button click"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = USER.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()
    
    return redirect('/users')

    

@app.post('/users/<int:user_id>/delete')
def delete_user_info(user_id):
    """Delete user info based on user ID"""

    USER.query.filter(USER.id == user_id).delete()

    db.session.commit()

    return redirect('/users')

# END OF USER ROUTES

# POSTS ROUTES

@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Displays form for new posts for user"""

    user = USER.query.get_or_404(user_id)

    return render_template('new-post-form.html', user = user)

@app.post('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    """Adds new post from form"""

    title = request.form['post_title']
    content = request.form['post_content']

    post = Post(title = title, content = content, created_at = "2022-02-03 6:00", user_id = user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """Shows post detail that was clicked on"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = USER.query.get_or_404(user_id)

    return render_template('post-detail.html', post = post, user = user)

@app.get('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Displays edit post page"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = USER.query.get_or_404(user_id)

    return render_template('post-edit.html', post = post, user = user)

@app.post('/posts/<int:post_id>/edit')
def update_post(post_id):
    """Updates page and redirects to post detail page"""

    title = request.form['post_title']
    content = request.form['post_content']

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes post"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    Post.query.filter(Post.id == post_id).delete()

    db.session.commit()

    return redirect(f'/users/{user_id}')