from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Configure sqlalchemy
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db =  SQLAlchemy(app)

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    hash = db.Column(db.String(100), unique=True, nullable=False)
    poem_count = db.Column(db.Integer, nullable=False)
    saved_poem_count = db.Column(db.Integer)
    session_token = db.Column(db.String(100),unique=True, nullable=False)
    registry_date = db.Column(db.DateTime, nullable=False, default = datetime.now()) #.strftime("%d-%b-%Y")

    def get_id(self):
        return str(self.session_token)

class Drafts(db.Model):
    __tablename__ ="drafts"
    draft_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    draft_count = db.Column(db.Integer, nullable = False)
    poem_count = db.Column(db.Integer, nullable = False)
    rhyme_scheme = db.Column(db.String(50), nullable = False)
    title = db.Column(db.Integer)
    notes = db.Column(db.String)
    line_break = db.Column(db.Integer)
    save_date = db.Column(db.DateTime, nullable = False) #.strftime("%d-%b-%Y at %I:%M%p")
    edit_date = db.Column(db.DateTime) #.strftime("%d-%b-%Y at %I:%M%p")

class Drafts_Lines(db.Model):
    __tablename__="draft_lines"
    draft_lines_id = db.Column(db.Integer, primary_key = True)
    draft_id = db.Column(db.Integer, db.ForeignKey("drafts.draft_id"),  nullable = False)
    line_num = db.Column(db.Integer, nullable = False)
    line_text = db.Column(db.String, nullable = False)

class Poems(db.Model):
    __tablename__ ="poems"
    poem_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    poem_count = db.Column(db.Integer, db.ForeignKey("users.poem_count"), nullable = False)
    rhyme_scheme = db.Column(db.String(50), nullable = False)
    title = db.Column(db.Integer)
    line_break = db.Column(db.Integer)
    save_date = db.Column(db.DateTime, nullable = False) #.strftime("%d-%b-%Y at %I:%M%p")
    edit_date = db.Column(db.DateTime) #.strftime("%d-%b-%Y at %I:%M%p")

class Poems_Lines(db.Model):
    __tablename__="poem_lines"
    poem_lines_id = db.Column(db.Integer, primary_key = True)
    poem_id = db.Column(db.Integer, db.ForeignKey("poems.poem_id"),  nullable = False)
    line_num = db.Column(db.Integer, nullable = False)
    line_text = db.Column(db.String, nullable = False)
