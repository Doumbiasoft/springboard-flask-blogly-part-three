"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS!

class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"

    def get_users():
      return User.query
    
    def get_user_by_id(id):
      user = User.query.get_or_404(id)
      return user
    
    def get_full_name(self):
       return f"{self.first_name} {self.last_name}"
    
    def add_users(firstname, lastname, imageurl=''):
      user = User(first_name=firstname, last_name=lastname, image_url=imageurl)
      db.session.add(user)
      db.session.commit()
      return True
    
    def update_users(id,firstname, lastname, imageurl=''):
      
      user = User.query.get_or_404(id)
      user.first_name=firstname
      user.last_name=lastname
      user.image_url=imageurl

      db.session.add(user)
      db.session.commit()
      return True
    
    def delete_users(id):
      user = User.query.get_or_404(id)
      db.session.delete(user)
      db.session.commit()
      return True
      

class Post(db.Model):
    """Post Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    
    def __repr__(self):
        return f"<User {self.id} {self.title} {self.content} {self.friendly_date}>"
    
    def add_post(user_id, title, content,tags):
      user = User.query.get_or_404(user_id)
      new_post = Post(title=title,
                    content=content,
                    user=user,
                    tags=tags)
      db.session.add(new_post)
      db.session.commit()
      return new_post
class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
        """Tag that can be added to posts."""

        __tablename__ = 'tags'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.Text, nullable=False, unique=True)

        posts = db.relationship('Post', secondary="posts_tags", cascade="all,delete", backref="tags")

    