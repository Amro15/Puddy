from email.policy import default
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# to migrate flask db upgrade
from flask_login import UserMixin
from datetime import datetime

from helpers import rhyme_scheme

# Configure sqlalchemy
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db =  SQLAlchemy(app)
Migrate = Migrate(app, db, render_as_batch=True)

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

# table that holds poem data until user decides to save
class CurrentUnsavedPoem(db.Model):
    __tablename__ = "current_unsaved_poem"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),  primary_key = True)
    current_rhymes = db.Column(db.String(), nullable=False, default="None")
    current_line_breaks = db.Column(db.Integer(), nullable=False, default=0)

class Drafts(db.Model):
    __tablename__ ="drafts"
    draft_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    draft_count = db.Column(db.Integer, nullable = False)
    poem_count = db.Column(db.Integer, nullable = False)
    rhyme_scheme = db.Column(db.String(50), nullable = False)
    rhymes = db.Column(db.String(), nullable = False)
    title = db.Column(db.Integer)
    notes = db.Column(db.String)
    line_break = db.Column(db.Integer)
    saved = db.Column(db.Integer, nullable=False, default=0)
    save_date = db.Column(db.DateTime, nullable = False) #.strftime("%d-%b-%Y at %I:%M%p")
    edit_date = db.Column(db.DateTime) #.strftime("%d-%b-%Y at %I:%M%p")

class DraftLines(db.Model):
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
    rhymes = db.Column(db.String(), nullable = False)
    title = db.Column(db.Integer)
    line_break = db.Column(db.Integer)
    save_date = db.Column(db.DateTime, nullable = False) #.strftime("%d-%b-%Y at %I:%M%p")
    edit_date = db.Column(db.DateTime) #.strftime("%d-%b-%Y at %I:%M%p")

class PoemLines(db.Model):
    __tablename__="poem_lines"
    poem_lines_id = db.Column(db.Integer, primary_key = True)
    poem_id = db.Column(db.Integer, db.ForeignKey("poems.poem_id"),  nullable = False)
    line_num = db.Column(db.Integer, nullable = False)
    line_text = db.Column(db.String, nullable = False)
