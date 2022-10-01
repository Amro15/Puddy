# from asyncio import constants
# from cgi import print_form
# from distutils.log import error
# from doctest import TestResults
# import email
# from email.mime import image
# from errno import EROFS
# from fileinput import filename
# import imp
# from operator import indexOf
# from optparse import SUPPRESS_USAGE
# from pickle import NONE
from asyncio.windows_events import NULL
from importlib.metadata import requires
import re
import random
# from xmlrpc import server
# from regex import F
import requests
# import urllib.parse
# from sre_parse import SPECIAL_CHARS
# from traceback import print_tb
# from types import MethodDescriptorType
# from urllib import response
# import uuid
# from winreg import REG_QWORD, QueryReflectionKey
# from wsgiref.simple_server import server_version
# from xml.sax.handler import all_properties
from flask import Flask, redirect, render_template, request, session, make_response, url_for, flash
from flask_session import Session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# from sqlalchemy import true
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
# import sqlite3
import os
# import urllib.request
# import json
import time
# import pandas as pd
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
from database import *

@login_manager.user_loader
def load_user(session_token):
    return Users.query.filter_by(session_token=session_token).first()
Session(app)

@app.route("/")
@login_required
def index():
    if session.get("request_logout", None)==True:
        session["request_logout"] = False
        logout_msg = True
    else:
        logout_msg = False
    return render_template("index.html", username=current_user.username, logout_msg = logout_msg)

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
        # if user is logged in request logout before accessing this page
        if current_user.is_authenticated:
            session["request_logout"] = True
            return redirect(url_for("index"))
        return render_template("register.html", form=form)
    if request.method == "POST":
        print("form errs:", form.errors)
        if form.validate_on_submit():
            # add user to db if form is valid(validation logic in forms.py)
            new_user = Users(username = form.username.data, hash=generate_password_hash(form.password.data), poem_count=0, saved_poem_count=0,
                            session_token = serializer.dumps(([form.username.data, generate_password_hash(form.password.data)])))
            db.session.add(new_user)
            db.session.commit()
            sigin_in_form = SigninForm()
            return render_template("signin.html", form=sigin_in_form, success_msg="Registered Successfully!")
        return render_template("register.html", form=form)

@app.route("/Signin", methods=["GET", "POST"])
def sign_in():
    # initialize form
    form = SigninForm()
    # if user is logged in request logout before accessing this page
    if request.method == "GET":
        if current_user.is_authenticated:
            session["request_logout"] = True
            return redirect(url_for("index"))
        return render_template("signin.html", form=form)

    if request.method == "POST":
        print(form.username.data, form.password.data)
        print("form errs:", form.errors)
        if form.validate_on_submit(): #validation logic in forms.py
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
        # check if user has a custom background store it in session to know which to render when rendering the page from post
        if os.path.exists("static/user_background.jpg"):
            user_background = "/static/user_background.jpg"
            session["user background"] = user_background
        else:
            user_background = "/static/create_write_background.jpg"
            session["user background"] = user_background
        return render_template("create.html", rhyme_schemes=rhyme_schemes, user_background=user_background, user_rhyme_scheme=session.get("user rhyme scheme"))
    if request.method == "POST":
        # Fields that need special handling 
        SPCEIAL_RHYME_SCHEMES = ["Custom", "Free Verse(No Rhyme Scheme)"]
        FIXED_RHYME_SCHEMES = ["Limerick","Shakespearean Sonnet","Haiku","Free Verse","Custom","Terza Rima"]

        user_background = session.get("user background", None)
        # select menu value
        user_rhyme_scheme = request.form.get("rhyme_schemes_select_menu")
        user_repeats = request.form.get("rhyme_repetition")
        line_breaks = request.form.get("line_break_frequency")
        print("user rhyme shcme", user_rhyme_scheme)

        if user_rhyme_scheme == "Custom":
            print("user rs", user_rhyme_scheme)
            # get user input and clean it up
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
            # Transfrom user custom rhyme scheme into an array of single letters :"ABBA" => ["A","B","B","A"]
            n = 1
            split_string = [user_custom_rhymes[i:i+n]
                            for i in range(0, len(user_custom_rhymes), n)]
            # Add user input to rhyme scheme class
            rhyme_scheme_class = str_to_class(user_rhyme_scheme.replace(" ", "_"))
            rhyme_scheme_class.rhymes = split_string
            if line_breaks:
                rhyme_scheme_class.line_break_frequency = int(line_breaks)
            # This is only to return the user scheme if they make a mistake
            session["rhyme scheme"]= user_rhyme_scheme
            session["user rhyme scheme"]= split_string
            # Keep track of how many poems user is creating
            current_user.poem_count += 1
            db.session.commit()
            session["draft_num"] = None
            return redirect(url_for("write", rs=user_rhyme_scheme))

        if user_rhyme_scheme == "Free Verse":
            print("user rs", user_rhyme_scheme)
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
            rhyme_scheme_class = str_to_class(user_rhyme_scheme.replace(" ", "_"))
            print("line amoount", lines_amount)
            rhyme_scheme_class.rhymes = lines_amount
            if line_breaks:
                rhyme_scheme_class.line_break_frequency = int(line_breaks)
            print("user rhymes", rhyme_scheme_class.rhymes)
            session["rhyme scheme"] = user_rhyme_scheme
            # Keep track of how many poems user is creating
            # user = Users.query.filter_by(session_token=current_user.get_id()).first()
            current_user.poem_count += 1
            db.session.commit()
            session["draft_num"] = None
            return redirect(url_for("write", rs=user_rhyme_scheme))


        # if user chooses rhyme scheme that has pre defined rhyme scheme
        if user_rhyme_scheme not in SPCEIAL_RHYME_SCHEMES:
            if not user_rhyme_scheme or user_rhyme_scheme not in rhyme_schemes:
                return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = "Must choose a valid rhyme scheme",  user_background=user_background, )
            session["rhyme scheme"] = user_rhyme_scheme
            # get line break frequency from rhyme scheme class to determine maximum amount of repeats
            rhyme_scheme_class = str_to_class(user_rhyme_scheme.replace(" ", "_"))
            if rhyme_scheme_class.increment_by == 0:
                maximum_repetition= 100
            elif rhyme_scheme_class.increment_by == 1:
                maximum_repetition= 24
            elif rhyme_scheme_class.increment_by == 2:
                maximum_repetition= 12
            else:
                maximum_repetition = 0
            # check for invalid input
            if not user_repeats or not user_repeats.isnumeric() or int(user_repeats)<0 or int(user_repeats)>maximum_repetition:
                return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = f"Repetition must be a number between 0 and {maximum_repetition}",  user_background=user_background, )
            else:
                print("user_rs: ",user_rhyme_scheme)
                session["rhyme scheme"] = user_rhyme_scheme
                rhyme_scheme_class = str_to_class(user_rhyme_scheme.replace(" ", "_"))
                # if user rhyme scheme can be repeated add therepeats to the rhymes class
                if user_rhyme_scheme not in FIXED_RHYME_SCHEMES:
                    rhyme_scheme_class.repeats = int(user_repeats)
                # monorhyme accepts a line break input so we need to check that
                if user_rhyme_scheme == "Monorhyme":
                    if not line_breaks:
                        line_breaks = 0
                    else:
                        if line_breaks and int(line_breaks)>int(user_repeats) or int(line_breaks)<0:
                            return render_template("create.html", rhyme_schemes=rhyme_schemes, error_msg = "Line Break Error: Line does not exist",  user_background=user_background, )
                    if line_breaks:
                        rhyme_scheme_class.line_break_frequency = int(line_breaks)
                # Keep track of how many poems user is creating
                current_user.poem_count += 1
                db.session.commit()
                session["draft_num"] = None
                return redirect(url_for("write", rs=user_rhyme_scheme))

        


@app.route("/Write", methods=["POST", "GET"])
@login_required
def write():
    if request.method == "GET":
        print("get write")
        print(request.args.get("rs"))
        # check if user has a custom background
        if os.path.exists("static/user_background.jpg"):
            user_background = "/static/user_background.jpg"
        else:
            user_background = "/static/create_write_background.jpg"
        if request.args.get("draft"):
            draft_session = True
            poem_num = session.get("draft_poem_num", None)
            draft_num = session.get("draft_num", None)
            # turn it into a poem class 
            draft = Drafts.query.filter_by(user_id=current_user.id, draft_count=draft_num, poem_count=poem_num).first()
            draft_lines = Drafts_Lines.query.filter_by(draft_id=draft.draft_id).all()
            rhyme_scheme_class= None
            user_rhyme_scheme = None

        elif request.args.get("rs") :
            draft_session = False
            print("is rs")
            user_draft = None
            user_rhyme_scheme = session.get("rhyme scheme", None)
            rhyme_scheme_class = str_to_class(request.args.get("rs").replace(" ", "_"))
            print("rhyme scheme class rhyme",rhyme_scheme_class.rhymes)
            draft = None
            draft_lines = None
        else:
            return redirect(url_for("create"))
        return render_template("write.html", rhyme_schemes=rhyme_scheme_class, user_background=user_background, user_rhyme_scheme=user_rhyme_scheme
        ,draft_session = draft_session, draft=draft, draft_lines=draft_lines)
# ===================================================================================================================================
    if request.method == "POST":
        print("is post")
        if request.get_json():
            # takes request body and turns it into a python dict
            req = request.get_json()
            # save request value to know what action to take
            server_request = request.headers["Request"]
            print("server_request is:", server_request)
            print("request is:", req)
            # server_request RHYME  ============================================================================================================
            if server_request=="get rhyme" :
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
                # save initial request because following requests will only have instructions on what to do next 
               
                print("server_request is save draft")
                print("rquest is", req)
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
                global_poem_num = Users.query.filter_by(id=current_user.id).first().poem_count
                print("poem num inside save is", global_poem_num)
                # check if this is a new draft 
                existing_draft = Drafts.query.filter_by(user_id=current_user.id).all()
                # bool to determine if exists
                draft_exists = False
                for i in existing_draft:
                    if global_poem_num == i.poem_count:
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
                    # save draft to db
                    draft = Drafts(user_id=current_user.id,draft_count=session.get("draft_num",None),poem_count=global_poem_num, rhyme_scheme=session.get("rhyme scheme", None), title=global_title,notes=global_notes, line_break=line_breaks, save_date=datetime.now())
                    db.session.add(draft)
                    db.session.commit()
                    # save draft lines to db referncing draft_id we just saved
                    for key, value in global_initial_request.items():
                            print("Adding to db...")
                            draft_lines = Drafts_Lines(draft_id=Drafts.query.filter_by(user_id=current_user.id, draft_count=session.get("draft_num",None), poem_count=global_poem_num).first().draft_id, line_num=key, line_text=value )
                            db.session.add(draft_lines)
                            db.session.commit()
                    return make_response({"response":"Draft was saved"}, 200)
                # if draft exists tell the server
                else:
                    # if session.get("draft_session", None) == True:
                    if request.args.get("draft"):
                        global_poem_num = session.get("draft_poem_num", None)
                    return make_response({"response":"draft already exists"}, 200)
            # make a save of the draft having the same poem number but increasing the current draft number
            if server_request == "save another draft":
                print("server_request is save another draft")
                print("init request", global_initial_request)
                print(session.get("draft_num", None))
                last_draft_num = Drafts.query.filter_by(user_id=current_user.id, poem_count=global_poem_num).order_by(Drafts.draft_count.desc()).first()
                session["draft_num"]= last_draft_num.draft_count+1
                print("Draft num is: ", session.get("draft_num", None))
                # insert new draft
                new_draft = Drafts(user_id=current_user.id, draft_count=session.get("draft_num", None), poem_count=global_poem_num, rhyme_scheme=session.get("rhyme scheme", None), title=global_title, notes=global_notes,  save_date=datetime.now())
                db.session.add(new_draft)
                db.session.commit()
                for key, value in global_initial_request.items():
                    new_draft_lines = Drafts_Lines(draft_id=Drafts.query.filter_by(user_id=current_user.id, draft_count=session.get("draft_num",None), poem_count=global_poem_num).first().draft_id, line_num=key, line_text=value )
                    db.session.add(new_draft_lines)
                    db.session.commit()
                return make_response({"response":"saved duplicate"}, 200)
            # update the draft the user is in currently 
            if server_request == "update draft":
                print("server_request is upd draft")
                print("intial req", global_initial_request)
                # db = get_db()
                # cur = db.cursor()
                print("title inside update is", global_title)
                print("darft nm", session.get("draft_num", None))
                print("peomnum", global_poem_num)
                print("uid", session.get("user_id", None))
                # update most recent draft accoridingly
                updated_draft = Drafts.query.filter_by(user_id=current_user.id, draft_count=session.get("draft_num", None), poem_count=global_poem_num).first()
                updated_draft.title = global_title
                updated_draft.notes = global_notes
                updated_draft.edit_date = datetime.now()
                db.session.commit()
                for key, value in global_initial_request.items():
                    updated_draft_lines = Drafts_Lines.query.filter_by(draft_id=Drafts.query.filter_by(user_id=current_user.id, draft_count=session.get("draft_num",None), poem_count=global_poem_num).first().draft_id, line_num=key).first()
                    updated_draft_lines.line_text = value
                    db.session.commit()
                return make_response({"response":"updated draft"}, 200)
            # REQUEST FORMAT ============================================================================================================
            if  server_request == "format":
                    poem_title = req["title"]
                    del req["title"]
                    user_saved_poem_count = Users.query.filter_by(id=current_user.id).first()
                    user_saved_poem_count.saved_poem_count += 1
                    db.session.commit() 
                    print("user saved poem count",user_saved_poem_count.saved_poem_count)
                    session["poem_num"] = user_saved_poem_count.saved_poem_count
                    line_breaks = str_to_class((session.get("rhyme scheme", None).replace(" ","_"))).line_break_frequency
                    user_poem = Poems(user_id=current_user.id, poem_count=user_saved_poem_count.saved_poem_count, rhyme_scheme=session.get("rhyme scheme", None), title=poem_title, line_break = line_breaks, save_date=datetime.now())
                    db.session.add(user_poem)
                    db.session.commit()

                    for key, value in req.items():
                        user_poem_lines = Poems_Lines(poem_id=Poems.query.filter_by(user_id=current_user.id, poem_count = session.get("poem_num", None)).first().poem_id, line_num=key, line_text=value)
                        db.session.add(user_poem_lines)
                        db.session.commit()
                    return make_response({"response":"successful"})

@app.route("/Format", methods=["POST", "GET"])
def format():
    if request.method == "GET":
        user_poem = Poems.query.filter_by(user_id=current_user.id, poem_count=Users.query.filter_by(id=current_user.id).first().saved_poem_count).first()
        user_poem_lines = Poems_Lines.query.filter_by(poem_id=Poems.query.filter_by(user_id=current_user.id).first().poem_id).all()
        return render_template("format.html", user_poem = user_poem, user_poem_lines=user_poem_lines, username=current_user.username)
    if request.method == "POST":
        req = request.get_json()
        if request.headers["Request"] == "save poem":
            print("req is", req)
            user_poem = Poems.query.filter_by(user_id= current_user.id, poem_count=Users.query.filter_by(id=current_user.id).first().saved_poem_count).first()
            user_poem.title = user_poem.title
            user_poem_lines = Poems_Lines.query.filter_by(poem_id=user_poem.poem_id).all()
            ctr =0
            print(req)
            for key,value in req.items():
                if user_poem_lines[ctr]:
                    user_poem_lines[ctr].line_text = value
                ctr+=1
            db.session.commit()
            return make_response({"response":"successful"})


@app.route("/Rhyme", methods=["POST", "GET"])
def rhyme():
    if request.method == "GET":
        return render_template("rhyme.html")
    if request.method == "POST":
        return render_template("rhyme.html")

# Account dropdown
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
        drafts = Drafts.query.filter_by(user_id=current_user.id).order_by(Drafts.poem_count.asc()).all()
        return render_template("draft.html", drafts=drafts)
    if request.method == "POST":
        req = request.get_json()
        if "draft_resume" in req.keys():
            print("Resume")
            for key, value in req.items():
                # set the draft poem num not to be mistaken with out session poem number which is just a counter
                session["draft_poem_num"] = str(value).split(";")[0]
                session["draft_num"] = str(value).split(";")[1]
            print("request is", req)
            print("in reusme", str(value).split(";")[0])
            print("poem num in resume draft", session.get("draft_poem_num"), None)
            return make_response({"respone":"Values stored"})
        if "draft_delete" in req.keys():
            print("Delete")
            for key, value in req.items():
                poem_num = str(value).split(";")[0]
                draft_num = str(value).split(";")[1]
            draft_title = Drafts.query.filter_by(user_id=current_user.id, poem_count=poem_num, draft_count=draft_num).first().title
            Drafts_Lines.query.filter_by(draft_id=Drafts.query.filter_by(user_id=current_user.id, poem_count=poem_num, draft_count=draft_num).first().draft_id).delete()
            Drafts.query.filter_by(user_id=current_user.id, poem_count=poem_num, draft_count=draft_num).delete()
            db.session.commit()
            return{"response":"Draft Deleted", "draft_title":draft_title, "draft_num":draft_num , "poem_num":poem_num}

# <div class="poem_container_account" id="container{{i.title}}/{{i.poem_count}}">
#     <div id ="account_poem">
#     <p id="poem_title" class="edit_line">{{i.title}}</p>
#     <p id="poem_author">By {{username}}</p>
# {%for key, value in data_arr[i].get_lines().items()%}
# <p id="{{key}}" class="edit_line" >{{value}}</p>
#     {% if data_arr[i].get_line_breaks() and ((loop.index%data_arr[i].get_line_breaks()) == 0)%}
#     <br>
#     <br>
#     {%endif%}
# {%endfor%}
# </div>
@app.route("/Account/Poem", methods=["POST", "GET"])
@login_required
def poems():
    if request.method == "GET":
        user_poems = Poems.query.filter_by(user_id=current_user.id).all()
        return render_template("poem.html", user_poems=user_poems, username=current_user.username)
    if request.method == "POST":
        req=request.get_json()
        if request.headers["Request"] == "delete poem":
            print("del poem")
            poem_id = req["poem_id"]
            poem = Poems.query.filter_by(user_id=current_user.id, poem_count=poem_id)
            print(poem_id)
            poem_title = poem.first().title
            poem_num = poem.first().poem_count
            Poems_Lines.query.filter_by(poem_id=poem.first().poem_id).delete()
            poem.delete()
            db.session.commit()
            return make_response({"response":"successful", "poem_title":poem_title,"poem_num":poem_num})
