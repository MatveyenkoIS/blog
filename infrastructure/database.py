from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserModel(db.Model):
    """Модель пользователя для базы данных."""
    
    __tablename__ = 'user_model'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('PostModel', backref='author', cascade='all, delete-orphan')
    comments = db.relationship('CommentModel', backref='author', cascade='all, delete-orphan')


class PostModel(db.Model):
    """Модель публикации для базы данных."""
    
    __tablename__ = 'post_model'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    comments = db.relationship('CommentModel', backref='post', cascade='all, delete-orphan')


class CommentModel(db.Model):
    """Модель комментария для базы данных."""
    
    __tablename__ = 'comment_model'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post_model.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)