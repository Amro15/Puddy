from asyncio import constants
from asyncio.windows_events import NULL
from cgi import print_form
from curses.ascii import isalnum, isalpha
from distutils.log import error
from doctest import TestResults
import email
from email.mime import image
from errno import EROFS
from fileinput import filename
import imp
from operator import indexOf
from optparse import SUPPRESS_USAGE
from pickle import NONE
import re
import random
from xmlrpc import server
import requests
import urllib.parse
from sre_parse import SPECIAL_CHARS
from traceback import print_tb
from types import MethodDescriptorType
from urllib import response
import uuid
from winreg import REG_QWORD, QueryReflectionKey
from wsgiref.simple_server import server_version
from xml.sax.handler import all_properties
from flask import Flask, redirect, render_template, request, session, jsonify, make_response, url_for, flash
from flask_session import Session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import sqlite3
import os
import urllib.request
import json
import time
import pandas as pd
from flask_wtf.csrf import CSRFProtect
from itsdangerous.url_safe import URLSafeSerializer


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "placeholder"
serializer= URLSafeSerializer(app.secret_key)
app.config["USE_SESSION_FOR_NEXT"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sign_in"
login_manager.login_message = "Please Sign In To Access The Rest Of The Website"


from helpers import *
from forms import *

@login_manager.user_loader
def load_user(session_token):
    return Users.query.filter_by(session_token=session_token).first()
Session(app)

@app.route("/")
@login_required
def index():
    user = Users.query.filter_by(session_token=current_user.get_id()).first()
    print(user)
    # username = query_db(
    #         "SELECT * FROM users WHERE id = ?", [session.get("user_id", None)], one=True)
    return render_template("index.html", username=user.username)

# error handling pages
@app.errorhandler(404)
def err_404(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def err_500(e):
    return render_template("500.html"), 500

@app.route("/Register", methods=["GET", "POST"])
def register():
    # initialize form
    form = RegisterForm()
    if request.method == "GET":
        return render_template("register.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            # add user to db if form is valid
            new_user = Users(username = form.username.data, hash=generate_password_hash(form.password.data), poem_count=0,
                            session_token = serializer.dumps(([form.username.data, generate_password_hash(form.password.data)])))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("sign_in"))
        return render_template("register.html", form=form)
        
            # db = get_db()
            # cur = db.cursor()
            # insert user into database
            # keep track of poem_num of user which we will need when saving users data
            # cur.execute("INSERT INTO users (username, hash, poem_count) VALUES(?, ?, ?)",
            #             (form.username.data, generate_password_hash(form.password.data), 0))
            # db.commit()
            # cur.close()
    

@app.route("/Signin", methods=["GET", "POST"])
def sign_in():
    form = SigninForm()
    if request.method == "GET":
        return render_template("signin.html", form=form)

    if request.method == "POST":
        print("Form valid", form.validate_on_submit())
        print(form.username.data, form.password.data)
        print("forsm errs:", form.errors)
        if form.validate_on_submit():
            print("validated")
            user = Users.query.filter_by(username = form.username.data).first()
            print(form.remember_me.data)
            login_user(user, remember = form.remember_me.data)
            session["user_id"] = user.id
            session["current_poem_num"] = user.poem_count

            if "next" in session:
                next = session["next"]
                if next!=None and is_safe_url(next):
                    return redirect(next)
            return redirect(url_for("index"))
        return render_template("signin.html", form=form)
            
            # username = request.form.get("username")
            # print(username)
            # password = request.form.get("password")
            # # check for blank inputs
            # if not username:
            #     return render_template("signin.html", error_msg="must provide username")

            # elif not password:
            #     return render_template("signin.html", error_msg="must provide password")


            # # # Ensure username exists and password is correct
            # if not user_db_info or not user_db_info["username"]:
            #     return render_template("signin.html", error_msg="invalid username", username=username, password=password)
            # if not check_password_hash(user_db_info["hash"], password):
            #     return render_template("signin.html", error_msg="invalid password", username=username, password=password)
            # # set session id to user id
            

@app.route("/Signout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("sign_in"))


@app.route("/GetInspired", methods=["POST", "GET"])
def get_inspired():
    global server_response
    if request.method == "GET":
        if session.get("search", None)!= None:
            session["search"] = None
            return render_template("get_inspired.html", server_response=server_response)
        else:
            return render_template("get_inspired.html")
    if request.method == "POST":
        # read into our csv and return it as json
        req = request.get_json()
        print("request is", req)
        # csv_file = "static/PoetryFoundationData.csv"
        # poems = pd.read_csv(csv_file)
        if req["request"] == "search poem":
            query = req["query"]
            query = query.strip().replace(" ","%20")
            search_by = req["search by"]
            if not search_by:
                return make_response({"response":"empty"})
            server_response = []
            if search_by == "search_by_title":
                url = f"https://poetrydb.org/title,poemcount/{query};{10}"
                print(url)
                server_response = requests.get(url)
                print("srvr resp",server_response)
                server_response = server_response.json()
                session["search"] = True
                return make_response({"response":"success"})

                # capitalize first letter of every word
                # query = query.title()
                # for index, row in poems.iterrows():
                #     if query in row["Title"].title():
                #         server_response.append(row.to_json())
                # return make_response({"response":server_response})
            if search_by == "search_by_author":
                url = f"https://poetrydb.org/author,poemcount/{query};{10}"
                server_response = requests.get(url)
                server_response = server_response.json()
                session["search"] = True
                return make_response({"response":"success"})

                # capitalize first letter of every word
                # query = query.lower().title()
                # for index, row in poems.iterrows():
                #     if query in row["Poet"] :
                #         server_response.append(row.to_json())
                # return make_response({"response":server_response})
            if search_by == "search_by_poem":
                url = f"https://poetrydb.org/lines,poemcount/{query};{10}"
                server_response = requests.get(url)
                server_response = server_response.json()
                session["search"] = True
                return make_response({"response":"success"})

                # for index, row in poems.iterrows():
                #     if query in row["Poem"]:
                #         server_response.append(row.to_json())
                # return make_response({"response":server_response})
        if req["request"] == "random" :
            server_response = []
            random_poems = random.choices([row.to_json() for index, row in poems.iterrows()], k=10)
            print(random_poems)
            return make_response({"response": random_poems})


@app.route("/About")
def about():
    return render_template("about.html")

@app.route("/Create/", methods=["POST", "GET"])
@login_required
def create():
    if request.method == "GET":
        # check if user hasa custom background
        if os.path.exists("static/user_background.jpg"):
            user_background = "/static/user_background.jpg"
            session["user background"] = user_background
        else:
            user_background = "/static/create_write_background.jpg"
            session["user background"] = user_background
        return render_template("create.html", rhyme_schemes=rhyme_schemes, user_background=user_background, user_rhyme_scheme=session.get("user rhyme scheme"))
    if request.method == "POST":
        SPCEIAL_RHYME_SCHEMES = ["Custom", "Free Verse(No Rhyme Scheme)"]
        user_background = session.get("user background", None)
        user_rhyme_scheme = request.form.get("rhyme_schemes_select_menu")
        user_repeats = request.form.get("rhyme_repetition")
        line_breaks = request.form.get("line_break_frequency")
        print("user rhyme shcme", user_rhyme_scheme)
        if user_rhyme_scheme == "Custom":
            print("user rs", user_rhyme_scheme)
            # get user input and modify it
            user_custom_rhymes = request.form.get("user_custom_rhymes")
            user_custom_rhymes = user_custom_rhymes.upper().replace(" ", "")
            # check for invalid input
            if not user_custom_rhymes or not user_custom_rhymes.isalpha():
                return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = "Rhyme scheme is required and must only consist of letters",  user_background=user_background, )
            if len(user_custom_rhymes)>100:
                return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = "Rhyme scheme can only be 100 letters long",  user_background=user_background, )
            if not line_breaks:
                line_breaks = 0
            else:
                if line_breaks and int(line_breaks)>len(user_custom_rhymes) or int(line_breaks)<0:
                    return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = "Line Break Error: Line does not exist",  user_background=user_background, )
            n = 1
            split_string = [user_custom_rhymes[i:i+n]
                            for i in range(0, len(user_custom_rhymes), n)]
            rhyme_scheme_class = user_rhyme_scheme.replace(" ", "_")
            rhyme_scheme_class = str_to_class(rhyme_scheme_class)
            rhyme_scheme_class.rhymes = split_string
            if line_breaks:
                rhyme_scheme_class.line_break_frequency = int(line_breaks)
            print("rhymes", rhyme_scheme_class.rhymes)
            print("Get id", rhyme_scheme_class.get_ids())
            print("brs",line_breaks)
            print("brs in class", rhyme_scheme_class.line_break_frequency)
            session["rhyme scheme"]= user_rhyme_scheme
            # This is only to return the user scheme if they make a mistake
            session["user rhyme scheme"]= split_string
            # poem_num used for storing user data later
            print(session.get("draft_session", None))
            if session.get("current_poem_num", None) == 0:
                session["current_poem_num"] = 1
            else:
                session["current_poem_num"] = int(session.get("current_poem_num", None))+1

            session["draft_session"] = False
            session["draft_num"] = None
            return redirect("/Write")
        if user_rhyme_scheme == "Free Verse":
            print(user_rhyme_scheme)
            # get user input
            lines = request.form.get("lines")
            # check for invalid input
            if not lines or not lines.isnumeric() or int(lines) < 0 or int(lines) > 100:
                return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = "Lines are required must be a whole number max is 100",  user_background=user_background, )
            if not line_breaks:
                line_breaks = 0
            else:
                if line_breaks and int(line_breaks)>int(lines) or int(line_breaks)<0:
                    return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = "Line Break Error: Line does not exist",  user_background=user_background, )
            lines_amount = []
            # enumarte lines starting at 1
            for i in range(int(lines)+1):
                if i != 0:
                    lines_amount.append(i)
            rhyme_scheme_class = user_rhyme_scheme.replace(" ", "_")
            rhyme_scheme_class = str_to_class(rhyme_scheme_class)
            rhyme_scheme_class.rhymes = lines_amount
            if line_breaks:
                rhyme_scheme_class.line_break_frequency = int(line_breaks)
            print("user rhymes", rhyme_scheme_class.rhymes)
            session["rhyme scheme"] = user_rhyme_scheme
            # current_poem_num used for storing user data later
            if session.get("current_poem_num", None) == 0:
                session["current_poem_num"] = 1
            else:
                session["current_poem_num"] = int(session.get("current_poem_num", None))+1
            session["draft_session"] = False
            session["draft_num"] = None
            return redirect("/Write")
        # if user chooses rhyme scheme that has pre defined rhyme scheme
        if user_rhyme_scheme not in SPCEIAL_RHYME_SCHEMES:
            if not user_rhyme_scheme or user_rhyme_scheme not in rhyme_schemes:
                return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = "Must choose a valid rhyme scheme",  user_background=user_background, )
            session["rhyme scheme"] = user_rhyme_scheme
            rhyme_scheme_class = user_rhyme_scheme.replace(" ", "_")
            rhyme_scheme_class = str_to_class(rhyme_scheme_class)
            if rhyme_scheme_class.increment_by == 0:
                maximum_repetition= 100
            elif rhyme_scheme_class.increment_by == 1:
                maximum_repetition= 24
            elif rhyme_scheme_class.increment_by == 2:
                maximum_repetition= 12
            else:
                maximum_repetition = 0
            if not user_repeats or not user_repeats.isnumeric() or int(user_repeats)<0 or int(user_repeats)>maximum_repetition:
                return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = f"Repetition must be a number between 0 and {maximum_repetition}",  user_background=user_background, )
            else:
                print(user_rhyme_scheme)
                session["rhyme scheme"] = user_rhyme_scheme
                rhyme_scheme_class = user_rhyme_scheme.replace(" ", "_")
                rhyme_scheme_class = str_to_class(rhyme_scheme_class)
                if user_rhyme_scheme not in FIXED_RHYME_SCHEMES:
                    rhyme_scheme_class.repeats = int(user_repeats)
                if user_rhyme_scheme == "Monorhyme":
                    if not line_breaks:
                        line_breaks = 0
                    else:
                        if line_breaks and int(line_breaks)>int(user_repeats) or int(line_breaks)<0:
                            return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = "Line Break Error: Line does not exist",  user_background=user_background, )
                    if line_breaks:
                        rhyme_scheme_class.line_break_frequency = int(line_breaks)
                # current_poem_num used for storing user data later
                print("draft sess?", session.get("draft_session", None))
                if session.get("current_poem_num", None) == 0:
                    db = get_db()
                    cur = db.cursor()
                    cur.execute("UPDATE users SET poem_count = ? WHERE id =?", (1, session.get("user_id", None)))
                    cur.close()
                    db.commit()
                    print(session.get("user_id", None))
                    row = query_db("SELECT * FROM users WHERE id = ?",[session.get("user_id", None)], one=True)
                    session["current_poem_num"] = row["poem_count"]
                else:
                    db = get_db()
                    cur = db.cursor()
                    print(session.get("current_poem_num", None))
                    cur.execute("UPDATE users SET poem_count = ? WHERE id =?",( int(session.get("current_poem_num", None))+1, session.get("user_id", None)))
                    cur.close()
                    db.commit()
                    row = query_db("SELECT * FROM users WHERE id = ?",[session.get("user_id", None)], one=True)
                    session["current_poem_num"] = row["poem_count"]
            
                session["draft_session"] = False
                session["draft_num"] = None
                return redirect("/Write")
        


@app.route("/Write", methods=["POST", "GET"])
@login_required
def write():
    if request.method == "GET":
        print("get write")
        # check if user has a custom background
        if os.path.exists("static/user_background.jpg"):
            user_background = "/static/user_background.jpg"
        else:
            user_background = "/static/create_write_background.jpg"
        print("draft sess in write is: ", session.get("draft_session", None))
        if session.get("draft_session", None) == True:
            poem_num = session.get("draft_poem_num", None)
            draft_num = session.get("draft_num", None)
            # turn it into a poem class to be easily accessible inside jinja
            user_draft = draft(str(poem_num)+str(draft_num), poem_num, draft_num)
            user_rhyme_scheme = user_draft.get_rhyme_scheme()
            rhyme_scheme_class = str_to_class(user_rhyme_scheme.replace(" ", "_"))
        else:
            user_draft = None
            user_rhyme_scheme = session.get("rhyme scheme", None)
            if user_rhyme_scheme != None:
                rhyme_scheme_class = user_rhyme_scheme.replace(" ", "_")
                rhyme_scheme_class = str_to_class(rhyme_scheme_class)
            else:
                return redirect(url_for("create"))
        # add poem = poem
        # , draft_session = session.get("draft_session", None))
        return render_template("write.html", rhyme_schemes=rhyme_scheme_class, user_background=user_background, user_rhyme_scheme=user_rhyme_scheme
        , draft=user_draft, draft_session = session.get("draft_session", None))
# ===================================================================================================================================
    if request.method == "POST":
        if request.get_json():
            # takes request body and turns it into a python dict
            req = request.get_json()
            # save request value to know what action to ake
            server_request = req["request"]
            # remove it so it doesn't interfere with our algorithm
            del req["request"]
            print("server_request is:", server_request)
            print("request is:", req)
            # server_request RHYME  =========================================================================================================
            if server_request=="get rhyme":
                server_response_rhymes = {"green":[], "yellow":[], "blue":[], "red":[]}
                # green rhymes / yellow rhymes but also rhymes with another rhyme group /
                #  blue pairs of words rhyme with each other but they don't all rhyme  / red doesn't rhyme
                # filter request of speical characters and whitespaces while counting empty values like A:["","","word","word","",""] 
                empty_rhymes = {}
                for key, value in req.items():
                    print(key)
                    req[key] = []
                    for i in value:
                        check_i = re.sub(r"[\s]", "", i)
                        if check_i == "":
                            req[key].append(None)
                            if key not in empty_rhymes:
                                empty_rhymes[key] = 1
                            else:
                                empty_rhymes[key] +=1
                        else:
                            if key not in empty_rhymes:
                                empty_rhymes[key] = 0
                            new_i = re.sub(r"[^\w\s'-]", "", i).lower().split()
                            req[key].append(new_i[len(new_i)-1])
                print("filtered request: ", req)
                print(empty_rhymes)
                # check which words rhyme with each other
                rhymes_checking_result = dict()
                for key, value in req.items():
                    if key and value :
                        for i in range(len(value)):
                            for j in range(len(value)):
                                if i != j and value[i]!=None and value[j]!=None:
                                    if isRhyme(req[key][i],req[key][j],1):
                                        rhymes_checking_result[str([key+str(i), key+str(j)])] = True
                                    else:
                                        rhymes_checking_result[str([key+str(i), key+str(j)])] = False
                print("rhyme_checking_result: ", rhymes_checking_result)

                # get elements ids for JS
                elements_id = {}
                for key, value in req.items():
                    elements_id[key] = []            
                    for i in range(len(value)):
                        elements_id[key].append(key+str(i))
                # print("elements_id: ", elements_id)

                # find dominant rhymes in each rhyme group
                rhyme_frequency = {}
                ctr = 0
                for key1, value1 in elements_id.items():
                    for i in value1:
                        ctr = 0
                        for key2, value2 in rhymes_checking_result.items():
                                if value2==True and i in key2:
                                            ctr+=1
                                            rhyme_frequency[i] = ctr
                                if value2==False and i in key2 and i not in server_response_rhymes["red"]:
                                    server_response_rhymes["red"].append(i)

                print("Wrongs:",server_response_rhymes)

                print("rhyme_frequency: ",rhyme_frequency)

                # make sure all words in rhyme group rhyme with each other and if they don't return it in our response
                # ex: A: flee,glee,night,fright is not accepted
                # val1<(len(req[key1[0]])-empty_rhymes[key1[0]]) since we want to ignore the empty spaces so we don't get wrong results
                for key1, val1 in rhyme_frequency.items():
                    for key2, val2 in rhyme_frequency.items():
                        if val1 == val2 and key1[0]==key2[0] and val1<(len(req[key1[0]])-empty_rhymes[key1[0]]) and key1 not in server_response_rhymes["blue"] and len(req[key1[0]])>3:
                                    server_response_rhymes["blue"].append(key1) 

                # print("server_response_rhymes: ", server_response_rhymes)

                # continue finding dominant rhyme in rhyme group
                largest = {}
                largest_results = []
                ctr = 0
                for key, val in rhyme_frequency.items():
                    ctr+=1
                    letter = key[0]
                    if val > largest.get(letter, -float('inf')) and key not in server_response_rhymes["blue"]:
                        largest[letter] = val        
                # print("lagrest", largest)
                for key, val in rhyme_frequency.items():
                    letter = key[0]
                    if letter in largest and largest[letter] == val: 
                        largest_results.append(key)
                # print("largest_results: ",largest_results)

                # check if rhymes are unique in each field : rhyme A cannot rhyme with B etc...
                check_unique = []
                for key1, value1 in req.items():
                    # print("k1: ", key1)
                    for i in range(len(value1)):
                        for key2, value2 in req.items():
                            # print("k2: ", key2)
                            for j in range(len(value2)):
                                if key1==key2:
                                    break
                                if isRhyme(value1[i], value2[j], 1) and key1+str(i) not in server_response_rhymes["red"] and key2+str(j) not in server_response_rhymes["red"]:
                                    print("keys: ",key1+str(i),key2+str(j))
                                    # print("check condition", key2+str(j),key2+str(j+1))
                                    # print(rhymes_checking_result[str([key2+str(j),key2+str(j+1)])]==True)
                                    check_unique.append([key1+str(i), key2+str(j)])
                                    break
                # print("check_unique: ",check_unique)

                # return results to the server
                for i in range(len(check_unique)):
                    for j in range(len(check_unique[i])):
                        if check_unique[i][j] in largest_results and check_unique[i][j] not in server_response_rhymes["yellow"]:
                            server_response_rhymes["yellow"].append(check_unique[i][j])
                for k in largest_results:
                    if k not in server_response_rhymes["green"] and k not in server_response_rhymes["yellow"]:
                            server_response_rhymes["green"].append(k)
                print("server_response_rhymes: ", server_response_rhymes)
                # print("server_response_rhymes: ", server_response_rhymes)
                # this creates a json response to return  to the frontend
                rhymes_resp = make_response((server_response_rhymes), 200)
                print(rhymes_resp.data)
                return rhymes_resp

            # server_request SYLLABLES==========================================================================================================
            if server_request == "get syllables":
                server_response_syllables = {}
                # put each value into an array since stringifying files with JSON turns arrays of length 1 into a string
                for key, value in req.items():
                    req[key] = []
                    req[key].append(value)
                # split sentence into words
                for key, value in req.items():
                    for i in value:
                        check_i_syllables = re.sub(r"[\s]", "", i)
                        # print("new i is: ", check_i_syllables)
                        if check_i_syllables != "":
                            # print("new inside: ", i)
                            new_i_syllables = re.sub(r"[^\w\s'-]", "", i).lower().split()
                            # print("insid after modification is:", new_i_syllables)
                            req[key] = new_i_syllables
                print("req after splitting: ", req)
                # get syallble count of each word
                server_response_syllables={}
                for key, value in req.items():
                    server_response_syllables[key] = []
                    for i in value:
                        syllable_count  = count_syllables(i)
                        server_response_syllables[key].append(syllable_count)
                print("server response is: ", server_response_syllables)
                syllables_resp = make_response((server_response_syllables), 200)
                return syllables_resp
            # server_request DRAFT ===============================================================================================================
            if server_request =="save draft":
                # save initial request because following requests will only have instructions on what to do next and not the input data
               
                print("server_request is save draft")
                print("rquest is", req)
                db = get_db()
                cur = db.cursor()
                # make vars global so we don't have to keep sending them in the following requests
                global global_title, global_poem_num, global_initial_request, global_notes
                global_title = req["title"]
                print("gloabl title", global_title)
                if not global_title:
                    global_title = "None"
                    print("title was none")
                del req["title"]
                global_notes = req["notes"]
                if not global_notes:
                    global_notes = "None"
                    print("no notes")
                del req["notes"]
                global_initial_request = req
                user_id = session.get("user_id", None)
                global_poem_num = session.get("current_poem_num", None)
                rhyme_scheme = session.get("rhyme scheme", None)
                print("poem num inside save is", global_poem_num)
                # check if this is a new draft 
                existing_draft = query_db("SELECT * FROM draft WHERE user_id = ?", [user_id])
                # bool to determine if exists
                draft_exists = False
                for i in existing_draft:
                    if global_poem_num == i["poem_num"]:
                        draft_exists = True
                        break
                # if there are no drafts of our current poem make a new one
                if not draft_exists :
                    print("draft doesn t exist")
                    print("title is", global_title)
                    print("gloabl peom num", global_poem_num)
                    session["draft_num"] = 1
                    print("draft num after adding to it", session.get("draft_num", None))
                    class_id = session.get("rhyme scheme", None).replace(" ","_")
                    line_breaks = str_to_class((class_id)).line_break_frequency
                    print("line_breaks", line_breaks)
                    for key, value in global_initial_request.items():
                            print("Adding to db...")
                            cur.execute("INSERT INTO draft (user_id, draft_num, poem_num, rhyme_scheme, title, line_num, line_text, date, notes, line_breaks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (user_id, session.get("draft_num", None), global_poem_num, session.get("rhyme scheme", None), global_title, key, value, time.ctime(), global_notes, line_breaks))
                    db.commit()
                    cur.close()
                    return make_response({"response":"Draft was saved"}, 200)
                # if draft exists tell the server
                else:
                    if session.get("draft_session", None) == True:
                        global_poem_num = session.get("draft_poem_num", None)
                    return make_response({"response":"draft already exists"}, 200)
            # make a save of the draft having the same poem number but increasing the current draft number
            if server_request == "save another draft":
                print("server_request is save another draft")
                print("title is", global_title)
                print("init request", global_initial_request)
                db = get_db()
                cur = db.cursor()
                # increment draft num
                print(session.get("draft_num", None))
                last_draft_num = query_db("SELECT * FROM draft WHERE poem_num =? ORDER BY draft_num DESC", [global_poem_num], one=True)
                session["draft_num"]= int(last_draft_num["draft_num"])+1
                print("Draft num is: ", session.get("draft_num", None))
                # insert new draft
                for key, value in global_initial_request.items():
                    cur.execute("INSERT INTO draft (user_id, draft_num, poem_num, rhyme_scheme, title, line_num, line_text, date, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (session.get("user_id", None), session.get("draft_num", None), global_poem_num, session.get("rhyme scheme", None), global_title, key, value, time.ctime(), global_notes))
                db.commit()
                cur.close()
                return make_response({"response":"saved duplicate"}, 200)
            # update the draft the user is in currently 
            if server_request == "update draft":
                print("server_request is upd draft")
                print("intial req", global_initial_request)
                db = get_db()
                cur = db.cursor()
                print("title inside update is", global_title)
                print("darft nm", session.get("draft_num", None))
                print("peomnum", global_poem_num)
                print("uid", session.get("user_id", None))
                # update most recent draft accoridingly
                for key, value in global_initial_request.items():
                    print("user_id", session.get("user_id", None), "|draft_num", session.get("draft_num", None), "|poem_num", global_poem_num, "|rhyme_scheme", session.get("rhyme scheme", None), "|line_num", key, "|line_text", value)
                    cur.execute("UPDATE draft SET title=?, line_text=?, date=?, notes=? WHERE line_num =? AND user_id=? AND draft_num=? AND poem_num=?",
                     (global_title, value, time.ctime(), global_notes, key, session.get("user_id", None), session.get("draft_num", None), global_poem_num))
                db.commit()
                cur.close()
                return make_response({"response":"updated draft"}, 200)
            # REQUEST FORMAT ============================================================================================================
            if  server_request == "format":
                    poem_title = req["title"]
                    del req["title"]
                    # this counter keeps track of how mnay poems the user has saved
                    row = query_db("SELECT * FROM users WHERE id = ?",[session.get("user_id", None)], one=True)
                    if not row["saved_poem_count"]:
                        db = get_db()
                        cur = db.cursor()
                        cur.execute("UPDATE users SET saved_poem_count = ? WHERE id=? ",(1,session.get("user_id", None)))
                        session["poem_num"] = row["saved_poem_count"]
                        cur.close()
                        db.commit()
                    else:
                        db = get_db()
                        cur = db.cursor()
                        cur.execute("UPDATE users SET saved_poem_count=? WHERE id=? ",(int(row["saved_poem_count"])+1,session.get("user_id", None)))
                        row = query_db("SELECT * FROM users WHERE id = ?",[session.get("user_id", None)], one=True)
                        session["poem_num"] = row["saved_poem_count"]
                        cur.close()
                        db.commit()
                    db = get_db()
                    cur = db.cursor()
                    # check if it's a draft session
                    class_id = session.get("rhyme scheme", None).replace(" ","_")
                    line_breaks = str_to_class((class_id)).line_break_frequency
                    if session.get("draft_session", None) !=True:
                        poem_id = str(session.get("current_poem_num"))+str(0)
                        for key, value in req.items():
                            cur.execute("INSERT INTO poem (user_id, poem_num, poem_id, rhyme_scheme, title, line_num, line_text, date, line_breaks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (session.get("user_id", None), session.get("poem_num", None), poem_id, session.get("rhyme scheme", None), poem_title, key, value, time.ctime(), line_breaks))
                        db.commit()
                        cur.close()
                        return make_response({"response":"successful"})
                    # if it is a draft session make sure to get the draft poem number not the current poem number
                    else:
                        poem_id = str(session.get("draft_poem_num", None))+str(session.get("draft_num", None))
                        for key, value in req.items():
                            cur.execute("INSERT INTO poem (user_id, poem_num, poem_id, rhyme_scheme, title, line_num, line_text, date, line_breaks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (session.get("user_id", None), session.get("poem_num", None), poem_id, session.get("rhyme scheme", None), poem_title, key, value, time.ctime(), line_breaks))
                        db.commit()
                        cur.close()
                        return make_response({"response":"successful"})
            
@app.route("/Format", methods=["POST", "GET"])
def format():
    if request.method == "GET":
        if session.get("draft_session", None) !=True:
            poem_id = str(session.get("current_poem_num"))+str(0)
        else:
            poem_id = str(session.get("draft_poem_num", None))+str(session.get("draft_num", None))
        user_poem = poem(poem_id)
        row = query_db("SELECT * FROM users WHERE id =?",[session.get("user_id", None)], one=True)
        username = row["username"]
        return render_template("format.html", user_poem = user_poem, username=username)
    if request.method == "POST":
        if session.get("draft_session", None) !=True:
                poem_id = str(session.get("current_poem_num"))+str(0)
        else:
            poem_id = str(session.get("draft_poem_num", None))+str(session.get("draft_num", None))
        user_poem = poem(poem_id)
        req = request.get_json()
        if req["request"] == "get rhyme scheme":
            return make_response({"response":user_poem.get_rhyme_scheme()})
        if req["request"] == "save poem":
            print("req is", req)
            poem_title = req["title"]
            del req["request"]; del req["title"]
            for key, value in req.items():
                db = get_db()
                cur = db.cursor()
                cur.execute("UPDATE poem SET title=?, line_text=?, date=? WHERE  user_id =? AND poem_id = ? AND line_num =?",
                (poem_title, value, time.ctime(), session.get("user_id", None), poem_id, key))
            db.commit()
            cur.close()
            return make_response({"response":"successful"})


@app.route("/Rhyme", methods=["POST", "GET"])
def rhyme():
    if request.method == "GET":
        return render_template("rhyme.html")
    if request.method == "POST":
        return render_template("rhyme.html")

# Account dropdown
# this should be accessible only from inside my /account
@app.route("/Account/Customize", methods=["POST", "GET"])
@login_required
def customize():
    if request.method == "GET":
        return render_template("customize.html")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template("customize.html", error_msg="No file part")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template("customize.html", error_msg="No file was selected")
        if not allowed_file(file.filename):
            return render_template("customize.html", error_msg="wrong file format")
        if file and allowed_file(file.filename):
            filename = secure_filename(
                "user_background."+file.filename.rsplit('.', 1)[1].lower())
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # if file not jpg convert to jpg
            if file.filename.rsplit('.', 1)[1].lower() != "jpg":
                img = Image.open(os.path.join(UPLOAD_FOLDER, filename))
                jpg_img = img.convert("RGB")
                jpg_img.thumbnail((1920, 1080))
                jpg_img.save(os.path.join(
                    UPLOAD_FOLDER, "user_background.jpg"))
                # delete non jpg file
                os.remove(os.path.join(UPLOAD_FOLDER, filename))
        return redirect("/Create")

@app.route("/Account/Draft", methods=["POST", "GET"])
@login_required
def drafts():
    if request.method == "GET":
        db =get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM draft WHERE user_id =? ORDER BY poem_num", [session.get("user_id", None)])
        data_arr = []
        # class and funcction in helpers.py
        x = draft(NULL,NULL,NULL)
        # create draft objects with the data from our db
        for i in cur:
            if x.poem_draft != str(i["poem_num"])+str(i["draft_num"]):
                x = draft(str(i["poem_num"])+str(i["draft_num"]), i["poem_num"], i["draft_num"])
                data_arr.append(x)
        for j in range(len(data_arr)):
            print(data_arr[j].get_lines())
        return render_template("draft.html", data_arr=data_arr)
    if request.method == "POST":
        req = request.get_json()
        if "draft_resume" in req.keys():
            print("Resume")
            for key, value in req.items():
                # set the draft poem num not to be mistaken with out session poem number which is just a counter
                session["draft_poem_num"] = str(value).split(";")[0]
                session["draft_num"] = str(value).split(";")[1]
            # this is important to let write know to load our draft and not any template
            session["draft_session"] = True
            print("request is", req)
            print("in reusme", str(value).split(";")[0])
            print("draft sess in draft after resume pressed is: ", session.get("draft_session", None))
            print("poem num in resume draft", session.get("draft_poem_num"), None)
            return make_response({"respone":"Values stored"})
        if "draft_delete" in req.keys():
            print("Delete")
            for key, value in req.items():
                poem_num = str(value).split(";")[0]
                draft_num = str(value).split(";")[1]
            db =get_db()
            cur = db.cursor()
            cur.execute("DELETE FROM draft WHERE user_id =? AND poem_num = ? AND draft_num = ?",(session.get("user_id", None), poem_num, draft_num))
            cur.close()
            db.commit()
            return{"response":"Draft Deleted"}

@app.route("/Account/Poem", methods=["POST", "GET"])
@login_required
def poems():
    if request.method == "GET":
        db =get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM poem WHERE user_id =? ORDER BY poem_num", [session.get("user_id", None)])
        data_arr = []
        # class and funcction in helpers.py
        x = poem(NULL)
        # create draft objects with the data from our db
        for i in cur:
            if x.poem_id != str(i["poem_id"]):
                x = poem(str(i["poem_id"]))
                data_arr.append(x)
        for j in range(len(data_arr)):
            print(data_arr[j].get_lines())
        row = query_db("SELECT * FROM users WHERE id =?",[session.get("user_id", None)], one=True)
        username = row["username"]
        return render_template("poem.html", data_arr=data_arr, username=username)
    if request.method == "POST":
        req=request.get_json()
        if req["request"] == "delete_poem":
            print("del poem")
            del req["request"]
            # send js poem title and num to know which element to hide when user deletes it
            poem_id = req["poem_id"]
            user_poem = poem(poem_id)
            poem_title = user_poem.get_title()
            poem_num = user_poem.get_poem_num()
            db = get_db()
            cur = db.cursor()
            cur.execute("DELETE FROM poem WHERE user_id = ? AND poem_id = ?",(session.get("user_id", None), poem_id))
            cur.close()
            db.commit()
            return make_response({"response":"successful", "poem_title":poem_title,"poem_num":poem_num})
