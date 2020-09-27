from . import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(String(255))
    password_secure = db.Column(db.String(255))
    comment = db.relaionship('comment', backref = 'user', lazy = 'dynamic')
    pitch  = db.relationship('pitch', backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def veryfy_password(self,password):
        return check_password_hash(self.pass_secure,password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return f'User {self.username}'



class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    response = db.Column(db.String(255))
    pitch_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('pitch.id'))

    def save_comment(self):
        '''
        Function that saves a comment
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.order_by(Comments.timeposted.desc()).filter_by(pitch_id=id).all()
        return comment

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key = True)
    name = db.column(db.String(255))

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls,):
        categories = Category.query.all()
        return categories


class Pitch(db.Model):
    __tablename__ = 'pitch'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    category = db.Column(db.Integer,db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    comments = db.relationship('comment', backref = 'pitch', lazy = "dynamic")
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    content = db.Column(db.String(255))

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        pitch.all_pitch.clear()

    #Display Pitches

    def get_pitch(cls,id):
        pitch = Pitch.query.filer_by(category_id = id).all()
        return pitches




