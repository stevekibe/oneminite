from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User (UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index=True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship("Pitch", backref="user", lazy= "dynamic")
    comment = db.relationship("Comments", backref="user", lazy= "dynamic")
    vote = db.relationship("Votes", backref="user", lazy= "dynamic")

    
    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User{self.username}'


class PitchCategory(db.Model):
    '''
    category table
    '''
    __tablename__ = 'categories'

    #table columns
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    
    def save_category(self):
        '''
        saving the pitches
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls):
        categories = PitchCategory.query.all()
        return categories


class Pitch(db.Model):
    '''
    class pitch
    '''
    __tablename__ = 'pitche'

    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship("Comments", backref="pitche", lazy= "dynamic")
    vote = db.relationship("Votes", backref="pitche", lazy= "dynamic")


    def save_pitch(self):
        '''
        method for saving a pitch
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()

    def get_pitches(id):
        '''
        method for displaying pitches
        '''
        pitches = Pitch.query.filter_by(category_id=id).all()
        return pitches

class Comments(db.Model):
    '''
    class for comments
    '''
    __tablename__= 'comments'

    id = db.Column(db.Integer, primary_key = True)
    opinion = db.Column(db.String(255))
    time_posted = db.Column(db.DateTime, default= datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_comment(self):
        '''
        method for saving a comment
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.order_by(
            Comments.time_posted.desc()).filter_by(pitches_id=id).all()
    
        return comment
    
class Votes(db.Model):
    '''
    class to model votes 
    '''
    __tablename__='votes'

    id = db.Column(db. Integer, primary_key=True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_vote(self):
        '''
        method for saving a vote
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls,user_id,pitches_id):
        votes = Vote.query.filter_by(user_id=user_id, pitches_id=pitches_id).all()
        return votes
    