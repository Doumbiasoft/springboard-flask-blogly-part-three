"""Blogly application."""

from flask import Flask,redirect,render_template,request,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] ="azertyqwerty"
app.config['DEBUG_TB_INTERCEPT_REDIRECT'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.errorhandler(404)

def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    """Home page."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

@app.route("/users")
def users():
    """Users page."""
    users = User.get_users()
    users.order_by(User.last_name,User.first_name)
    return render_template("users/users.html",users=users.all(),count=users.count())

@app.route("/users/new")
def users_new():
    """Add user page."""
    return render_template("users/add.html")

@app.route("/users/new",methods=["POST"])
def users_new_add():
    """Send user data page."""
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    imageurl = request.form.get("imageurl")

    if firstname == "":
      flash(f"Fill the field First name")
      return redirect('/users/new')
    if lastname == "":
      flash(f"Fill the field Last name")
      return redirect('/users/new')
    else:
      ok = User.add_users(firstname, lastname, imageurl)
      if ok:
         flash(f"User '{firstname}' '{lastname}' added Successfully")
         return redirect('/users')
      else:
          return
      
@app.route("/users/<int:id>")
def users_details(id):
    """Details user page."""
    user = User.get_user_by_id(id)
    return render_template("users/details.html",user=user)

@app.route("/users/<int:id>/edit")
def users_edit(id):
    """Edit user page."""
    user = User.get_user_by_id(id)
    return render_template("users/edit.html",user=user)

@app.route("/users/<int:id>/edit",methods=["POST"])
def users_edit_save(id):
    """update user data page."""
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    imageurl = request.form.get("imageurl")

    if firstname == "":
      flash(f"Fill the field First name")
      return redirect(f"/users/{id}/edit")
    if lastname == "":
      flash(f"Fill the field Last name")
      return redirect(f"/users/{id}/edit")
    else:
      ok = User.update_users(id,firstname, lastname, imageurl)
      if ok:
         flash(f"User up to date Successfully")
         return redirect('/users')
      else:
          return

@app.route("/users/<int:id>/delete")
def delete_users(id):
    """delete user."""
    ok = User.delete_users(id)
    if ok:
         flash(f"User deleted successfully")
    return redirect('/users')


##############################################################################
# Posts route


@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = User.get_user_by_id(user_id)
    tags = Tag.query.all()
    return render_template('posts/add.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """New post for a user"""
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post= Post.add_post(user_id,request.form['title'],request.form['content'],tags)
    flash(f"Post '{new_post.title}' added Successfully.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Details a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post,tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited Successfully.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    """Deleting an existing post"""

    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title} deleted Successfully.")

    return redirect(f"/users/{post.user_id}")


##############################################################################
# Tags route


@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/tags.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/add.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added Successfully.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/details.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited Successfully.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete')
def tags_destroy(tag_id):
    """Deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted Successfully.")

    return redirect("/tags")
   