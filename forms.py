from flask import session
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length, ValidationError, Regexp
from database import db, Users


def check_username_dup(form, username):
    # make sure username is not already in db
    user = Users.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError("Username Is Taken")
            

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username Field Required"), 
                                                    Length(min=3, max=30, message="Username Must Contain 3 to 30 Characters"),
                                                    Regexp("^[A-Za-z][A-Za-z0-9_]{2,29}$", message="Username can only contain letter numbers and underscores and must start with a letter"),
                                                    check_username_dup])
                                                    
    password = PasswordField("Password", validators=[InputRequired(message="Password Field Required"),
                                                    EqualTo("cpassword", message="Passwords Don't Match"),
                                                    Regexp("^\S{8,40}$", message="Password Cannot Contain Spaces"),
                                                    Length(min=8, max=40, message="Password Must Contain 8 to 40 Characters")])

    cpassword = PasswordField("Confirm Password", validators=[InputRequired(message="Confirm Password Field Required")])
    register = SubmitField("Register")

def validate_usermame(form, username):
    # make sure username is in db
    user = Users.query.filter_by(username=username.data).first()
    print("user", user)
    if not user:
        print("not user")
        raise ValidationError("Incorrect Username")
def validate_password(form, password):
    # make sure password match with pass in db
    passwd = Users.query.filter_by(username=form.username.data).first()
    if passwd:
        print("check pass", check_password_hash(passwd.hash, password.data))
    if passwd and not check_password_hash(passwd.hash, password.data):
        print("not pass")
        raise ValidationError("Incorrect Password")

class SigninForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username Field Required"), validate_usermame])
    password = PasswordField("Password", validators=[InputRequired(message="Password Field Required"), validate_password])
    remember_me = BooleanField("Remember Me")
    sign_in = SubmitField("Sign In")