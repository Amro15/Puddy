import re
import requests
from flask import Flask, redirect, render_template, request, session, make_response, url_for, flash
from flask_session import Session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
import os
from flask_wtf.csrf import CSRFProtect
from flask_paginate import Pagination
from itsdangerous.url_safe import URLSafeSerializer
from datetime import datetime, timedelta


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "placeholder"
serializer = URLSafeSerializer(app.secret_key)
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
        print("form errs:", form.errors)
        if form.validate_on_submit():
            # add user to db if form is valid(validation logic in forms.py)
            new_user = Users(username=form.username.data, hash=generate_password_hash(form.password.data), poem_count=0, saved_poem_count=0,
                             session_token=serializer.dumps(([form.username.data, generate_password_hash(form.password.data)])))
            db.session.add(new_user)
            db.session.commit()
            # used to hold user data until user decides to save
            sigin_in_form = SigninForm()
            return render_template("signin.html", form=sigin_in_form, success_msg="Registered Successfully!")
        return render_template("register.html", form=form)


@app.route("/Signin", methods=["GET", "POST"])
def sign_in():
    # initialize form
    form = SigninForm()
    # if user is logged in request logout before accessing this page
    if request.method == "GET":
        return render_template("signin.html", form=form)

    if request.method == "POST":
        print(form.username.data, form.password.data)
        print("form errs:", form.errors)
        if form.validate_on_submit():  # validation logic in forms.py
            user = Users.query.filter_by(username=form.username.data).first()
            print(form.remember_me.data)
            login_user(user, remember=form.remember_me.data)
            session["user_id"] = user.id
            session["current_poem_num"] = user.poem_count

            if "next" in session:
                next = session["next"]
                if next != None and is_safe_url(next):
                    return redirect(next)
            return redirect(url_for("index"))
        return render_template("signin.html", form=form)


@app.route("/Signout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("sign_in"))


@app.route("/")
def index():
    return render_template("index.html")

# create poems with different preset rhyme schemes or using a custom one


@app.route("/Create/", methods=["POST", "GET"])
def create():
    if request.method == "GET":
        # check if user has a custom background store it in session to know which to render when rendering the page from post
        user_background = "/static/create_write_background.jpg"
        session["user background"] = user_background
        if current_user.is_authenticated and CurrentUnsavedPoem.query.filter_by(user_id=current_user.id).first():
            recent_poem = True
        else:
            recent_poem = False
        return render_template("create.html", rhyme_schemes=rhyme_schemes, user_background=user_background, recent_poem=recent_poem)
    if request.method == "POST":
        # Fields that need special handling
        SPCEIAL_RHYME_SCHEMES = ["Custom", "Free Verse, Blank Verse"]
        FIXED_RHYME_SCHEMES = ["Limerick", "Shakespearean Sonnet",
                               "Haiku", "Free Verse", "Custom", "Terza Rima"]

        user_background = session.get("user background", None)
        # select menu value
        user_rhyme_scheme = request.form.get("rhyme_schemes_select_menu")
        user_repeats = request.form.get("rhyme_repetition")
        line_breaks = request.form.get("line_break_frequency")
        print("user rhyme shcme", user_rhyme_scheme)

        # if rhyme scheme custom
        if user_rhyme_scheme == "Custom":
            # get user input and clean it up
            user_custom_rhymes = request.form.get("user_custom_rhymes")
            user_custom_rhymes = user_custom_rhymes.upper().replace(" ", "")
            # check for invalid input
            pattern = re.compile("[a-zA-Z-]+")
            if not user_custom_rhymes or pattern.match(str(user_custom_rhymes)) == None or not pattern.match(str(user_custom_rhymes)).group() == str(user_custom_rhymes):
                flash(
                    "Rhyme scheme is required and must only consist of letters or - (dash symbol)")
                return redirect(url_for("create"))
            if len(user_custom_rhymes) > 100:
                flash("Rhyme scheme can only be 100 letters long")
                return redirect(url_for("create"))
            print("BR", line_breaks)
            if not line_breaks:
                line_breaks = 0
            elif line_breaks and int(line_breaks) > len(user_custom_rhymes) or int(line_breaks) < 0:
                flash("Line Break Error: Line does not exist")
                return redirect(url_for("create"))
            print("BR after", line_breaks)
            # Transfrom user custom rhyme scheme into an array of single letters :"ABBA" => ["A","B","B","A"]
            n = 1
            split_string = [user_custom_rhymes[i:i+n]
                            for i in range(0, len(user_custom_rhymes), n)]
            # Add user input to rhyme scheme class
            rhyme_scheme_class = str_to_class(
                user_rhyme_scheme.replace(" ", "_"))
            rhyme_scheme_class.rhymes = split_string
            rhyme_scheme_class.line_break_frequency = int(line_breaks)
            # Keep track of how many poems user is creating and of user current rhyme scheme to check against unwanted inputs when saving
            if current_user.is_authenticated:
                current_user.poem_count += 1
                unsaved_poem = CurrentUnsavedPoem.query.filter_by(
                    user_id=current_user.id).first()
                rhymes = ",".join(rhyme_scheme_class.get_ids())
                if unsaved_poem:
                    unsaved_poem.rhymes = rhymes
                    unsaved_poem.rhyme_scheme = user_rhyme_scheme
                    print(unsaved_poem.rhymes)
                    unsaved_poem.line_break = line_breaks
                    print("unsaved brs", unsaved_poem.line_break)
                    db.session.commit()
                else:
                    unsaved_poems = CurrentUnsavedPoem(
                        user_id=current_user.id, rhyme_scheme=user_rhyme_scheme, rhymes=rhymes, line_break=line_breaks)
                    db.session.add(unsaved_poems)
                    db.session.commit()
            return redirect(url_for("write", rs=user_rhyme_scheme))

        # if rhyme scheme free verse
        if user_rhyme_scheme == "Free Verse" or user_rhyme_scheme == "Blank Verse":
            print("user rs", user_rhyme_scheme)
            # get user input
            lines = request.form.get("lines")
            # check for invalid input
            if not lines or not lines.isnumeric() or int(lines) < 0 or int(lines) > 100:
                flash("Lines are required and must be a whole number between 1 and 100")
                return redirect(url_for("create"))
            if not line_breaks:
                line_breaks = 0
            else:
                if line_breaks and int(line_breaks) > int(lines) or int(line_breaks) < 0:
                    flash("Line Break Error: Line does not exist")
                    return redirect(url_for("create"))
            lines_amount = []
            # enumarte lines starting at 1
            for i in range(int(lines)+1):
                if i != 0:
                    lines_amount.append(i)
            rhyme_scheme_class = str_to_class(
                user_rhyme_scheme.replace(" ", "_"))
            print("line amoount", lines_amount)
            rhyme_scheme_class.rhymes = lines_amount
            rhyme_scheme_class.line_break_frequency = int(line_breaks)
            print("user rhymes", rhyme_scheme_class.rhymes)
            # Keep track of how many poems user is creating and of user current rhyme scheme to check against unwanted inputs when saving
            if current_user.is_authenticated:
                current_user.poem_count += 1
                unsaved_poem = CurrentUnsavedPoem.query.filter_by(
                    user_id=current_user.id).first()
                # we use map to convert int array to string
                rhymes = ",".join(map(str, rhyme_scheme_class.get_ids()))
                if unsaved_poem:
                    unsaved_poem.rhymes = rhymes
                    unsaved_poem.rhyme_scheme = user_rhyme_scheme
                    unsaved_poem.line_break = line_breaks
                    db.session.commit()
                else:
                    unsaved_poems = CurrentUnsavedPoem(
                        user_id=current_user.id, rhyme_scheme=user_rhyme_scheme, rhymes=rhymes, line_break=line_breaks)
                    db.session.add(unsaved_poems)
                    db.session.commit()
            return redirect(url_for("write", rs=user_rhyme_scheme))

        # if user chooses rhyme scheme that has pre defined rhyme scheme
        if user_rhyme_scheme not in SPCEIAL_RHYME_SCHEMES:
            if not user_rhyme_scheme or user_rhyme_scheme not in rhyme_schemes:
                flash("Must choose a valid rhyme scheme")
                return redirect(url_for("create"))
            # get line break frequency from rhyme scheme class to determine maximum amount of repeats
            rhyme_scheme_class = str_to_class(
                user_rhyme_scheme.replace(" ", "_"))
            if rhyme_scheme_class.increment_by == 0:
                maximum_repetition = 100
            elif rhyme_scheme_class.increment_by == 1:
                maximum_repetition = 24
            elif rhyme_scheme_class.increment_by == 2:
                maximum_repetition = 12
            else:
                maximum_repetition = 0
            # check for invalid input
            if not user_repeats or not user_repeats.isnumeric() or int(user_repeats) < 0 or int(user_repeats) > maximum_repetition:
                flash(
                    f"Repetition must be a number between 0 and {maximum_repetition}")
                return redirect(url_for("create"))
            else:
                print("user_rs: ", user_rhyme_scheme)
                # session["rhyme scheme"] = user_rhyme_scheme
                rhyme_scheme_class = str_to_class(
                    user_rhyme_scheme.replace(" ", "_"))
                # if user rhyme scheme can be repeated add therepeats to the rhymes class
                if user_rhyme_scheme not in FIXED_RHYME_SCHEMES:
                    rhyme_scheme_class.repeats = int(user_repeats)
                # monorhyme accepts a line break input so we need to check that
                if user_rhyme_scheme == "Monorhyme":
                    if not line_breaks:
                        line_breaks = 0
                    else:
                        if line_breaks and int(line_breaks) > int(user_repeats) or int(line_breaks) < 0:
                            flash("Line Break Error: Line does not exist")
                            return redirect(url_for("create"))
                    rhyme_scheme_class.line_break_frequency = int(line_breaks)
                # Keep track of how many poems user is creating and of user current rhyme scheme to check against unwanted inputs when saving
                if current_user.is_authenticated:
                    current_user.poem_count += 1
                    unsaved_poem = CurrentUnsavedPoem.query.filter_by(
                        user_id=current_user.id).first()
                    if user_rhyme_scheme == "Haiku":
                        rhymes = ",".join(map(str, rhyme_scheme_class.rhymes))
                        print("Haiku", rhymes)
                    else:
                        rhymes = ",".join(rhyme_scheme_class.get_ids())
                    if unsaved_poem:
                        print("tehre s unsaved poem")
                        unsaved_poem.rhymes = rhymes
                        unsaved_poem.rhyme_scheme = user_rhyme_scheme
                        if user_rhyme_scheme == "Haiku":
                            unsaved_poem.line_break = 0
                        else:
                            unsaved_poem.line_break = rhyme_scheme_class.line_break_frequency
                        db.session.commit()
                    else:
                        unsaved_poems = CurrentUnsavedPoem(
                            user_id=current_user.id, rhyme_scheme=user_rhyme_scheme, rhymes=rhymes, line_break=line_breaks)
                        db.session.add(unsaved_poems)
                        db.session.commit()
                return redirect(url_for("write", rs=user_rhyme_scheme))


# check rhymes/check syllables/check meter/undo-save edits/ save-update-edit drafts/save-update-edit poems/
@app.route("/Write", methods=["POST", "GET"])
# @login_required
def write():
    if request.method == "GET":
        # check if user has a custom background
        if os.path.exists("static/user_background.jpg"):
            user_background = "/static/user_background.jpg"
        else:
            user_background = "/static/create_write_background.jpg"
        if request.args.get("rs"):
            user_rs = request.args.get("rs")
            write_session = "default"
            if user_rs not in rhyme_schemes:
                flash("Invalid Rhyme Scheme")
                return redirect(url_for("create"))
            if current_user.is_authenticated:
                rhyme_scheme = CurrentUnsavedPoem.query.filter_by(
                    user_id=current_user.id).first()
                if not rhyme_scheme or not (rhyme_scheme.rhyme_scheme == user_rs):
                    flash(
                        "Please Select A Rhyme Scheme From Create Before Heading To Write")
                    return redirect(url_for("create"))
                session["rs"] = rhyme_scheme.rhyme_scheme
                return render_template("write.html", rhyme_schemes=rhyme_scheme,
                                       user_rhyme_scheme=rhyme_scheme.rhyme_scheme, user_background=user_background, write_session=write_session,
                                       detatch_util=request.cookies.get("detatch_util"), hide_detatch_btn=request.cookies.get("hide_detatch_btn"), disable_reminder=request.cookies.get("disable_reminder"),
                                       skip_format=request.cookies.get("skip_format"))
            else:
                user_rhyme_scheme = user_rs
                session["rs"] = user_rhyme_scheme
                rhyme_scheme_class = str_to_class(user_rs.replace(" ", "_"))
                return render_template("write-guest.html", rhyme_schemes=rhyme_scheme_class, user_background=user_background, user_rhyme_scheme=user_rhyme_scheme)
        elif current_user.is_authenticated:
            request_args = False
            if request.args.get("resume"):
                request_args = True
                write_session = "resume"
                database = CurrentUnsavedPoem
                lines_database = CurrentUnsavedPoemLines
            elif request.args.get("draft"):
                request_args = True
                write_session = "draft"
                database = Drafts
                lines_database = DraftLines
            elif request.args.get("poem"):
                request_args = True
                write_session = "poem"
                database = Poems
                lines_database = PoemLines
            if request_args:
                if request.args.get("resume"):
                    poem = database.query.filter_by(
                        user_id=current_user.id).first()
                elif request.args.get("draft"):
                    poem = database.query.filter_by(
                        user_id=current_user.id, draft_id=request.args.get("draft")).first()
                elif request.args.get("poem"):
                    poem = database.query.filter_by(
                        user_id=current_user.id, poem_id=request.args.get("poem")).first()
                user_rhyme_scheme = poem.rhyme_scheme
                session["rs"] = user_rhyme_scheme
                title = poem.title
                if len(str(poem.line_break))!=1 :
                    line_breaks = poem.line_break.split(",")
                else:
                    line_breaks = poem.line_break
                if request.args.get("resume"):
                    poem_lines = lines_database.query.filter_by(
                        user_id=current_user.id).all()
                elif request.args.get("draft"):
                    poem_lines = lines_database.query.filter_by(
                        draft_id=poem.draft_id).all()
                elif request.args.get("poem"):
                    poem_lines = lines_database.query.filter_by(
                        poem_id=poem.poem_id).all()
                poem_lines_obj = {}
                for i in poem_lines:
                    poem_lines_obj[i.line_num] = i.line_text
                print("poem_lines_obj", poem_lines_obj)
                print("write br", line_breaks)
                return render_template("write.html", user_background=user_background,
                                       user_rhyme_scheme=user_rhyme_scheme, title=title, poem_lines=poem_lines_obj, line_breaks=line_breaks, write_session=write_session,
                                       detatch_util=request.cookies.get("detatch_util"), hide_detatch_btn=request.cookies.get("hide_detatch_btn"), disable_reminder=request.cookies.get("disable_reminder"),
                                       skip_format=request.cookies.get("skip_format"))
        else:
            return redirect(url_for("create"))
# ===================================================================================================================================
    if request.method == "POST":
        if request.get_json():
            # takes request body and turns it into a python dict
            req = request.get_json()
            # save request value to know what action to take
            server_request = request.headers["Request"]
            print("server_request is:", server_request)
            print("request is:", req)
            # server_request RHYME  ============================================================================================================
            if server_request == "get rhyme":
                server_response_rhymes = {"green": [],
                                          "yellow": [], "blue": [], "red": []}
                # green rhymes / yellow rhymes but also rhymes with another rhyme group /
                #  blue pairs of words rhyme with each other but they don't all rhyme  / red doesn't rhyme
                # filter request of speical characters and whitespaces while counting empty values like A:["","","word","word","",""]
                empty_rhymes = {}
                # delete lines that don t have a rhyme
                if "-" in req:
                    del req["-"]
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
                                empty_rhymes[key] += 1
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
                    if key and value:
                        for i in range(len(value)):
                            for j in range(len(value)):
                                if i != j and value[i] != None and value[j] != None:
                                    if isRhyme(req[key][i], req[key][j], 1):
                                        rhymes_checking_result[str(
                                            [key+str(i), key+str(j)])] = True
                                    else:
                                        rhymes_checking_result[str(
                                            [key+str(i), key+str(j)])] = False
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
                            if value2 == True and i in key2:
                                ctr += 1
                                rhyme_frequency[i] = ctr
                            if value2 == False and i in key2 and i not in server_response_rhymes["red"]:
                                server_response_rhymes["red"].append(i)

                print("Wrongs:", server_response_rhymes)

                print("rhyme_frequency: ", rhyme_frequency)

                # make sure all words in rhyme group rhyme with each other and if they don't return it in our response
                # ex: A: flee,glee,night,fright is not accepted
                # val1<(len(req[key1[0]])-empty_rhymes[key1[0]]) to ignore the empty spaces so we don't get wrong results
                for key1, val1 in rhyme_frequency.items():
                    for key2, val2 in rhyme_frequency.items():
                        if val1 == val2 and key1[0] == key2[0] and val1 < (len(req[key1[0]])-empty_rhymes[key1[0]]) and key1 not in server_response_rhymes["blue"] and len(req[key1[0]]) > 3:
                            server_response_rhymes["blue"].append(key1)

                # print("server_response_rhymes: ", server_response_rhymes)

                # continue finding dominant rhyme in rhyme group
                largest = {}
                largest_results = []
                ctr = 0
                for key, val in rhyme_frequency.items():
                    ctr += 1
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
                                if key1 == key2:
                                    break
                                if isRhyme(value1[i], value2[j], 1) and key1+str(i) not in server_response_rhymes["red"] and key2+str(j) not in server_response_rhymes["red"]:
                                    print("keys: ", key1+str(i), key2+str(j))
                                    # print("check condition", key2+str(j),key2+str(j+1))
                                    # print(rhymes_checking_result[str([key2+str(j),key2+str(j+1)])]==True)
                                    check_unique.append(
                                        [key1+str(i), key2+str(j)])
                                    break
                # print("check_unique: ",check_unique)

                # return results to the server
                for i in range(len(check_unique)):
                    for j in range(len(check_unique[i])):
                        if check_unique[i][j] in largest_results and check_unique[i][j] not in server_response_rhymes["yellow"]:
                            server_response_rhymes["yellow"].append(
                                check_unique[i][j])
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
                            new_i_syllables = re.sub(
                                r"[^\w\s'-]", "", i).lower().split()
                            # print("insid after modification is:", new_i_syllables)
                            req[key] = new_i_syllables
                print("req after splitting: ", req)
                # get syallble count of each word
                server_response_syllables = {}
                for key, value in req.items():
                    server_response_syllables[key] = []
                    for i in value:
                        syllable_count = count_syllables(i)
                        server_response_syllables[key].append(syllable_count)
                print(session.get("rs", None))
                if session.get("rs", None) == "Haiku":
                    server_response_syllables["rs"] = "Haiku"
                if session.get("rs", None) == "Shakespearean Sonnet":
                    server_response_syllables["rs"] = "Shakespearean Sonnet"
                print("server response is: ", server_response_syllables)
                syllables_resp = make_response(
                    (server_response_syllables), 200)
                return syllables_resp

            # server_request METER ===================================================================================================================
            if server_request == "check meter":
                server_meter_response = {}
                for key, value in req.items():
                    server_meter_response[key]=str(check_meter(value))
                print(server_meter_response)
                return make_response(server_meter_response, 200)

            # server request undo edits =================================================================================================================================
            if server_request == "undo edits":
                # get the initial lines the user used in create and render them with any text that may be in them
                title = req["title"]
                notes = req["notes"]
                line_breaks = req["line_breaks"]
                del req["title"]; del req["notes"]; del req["line_breaks"]
                poem = CurrentUnsavedPoem.query.filter_by(
                    user_id=current_user.id).first()
                rhyme_check = poem.rhymes.split(",")
                filtered_req = []
                ctr = 0
                # only check for rhymes user started with
                for key, value in req.items():
                    if ctr < (len(rhyme_check)):
                        filtered_req.append(value)
                    ctr += 1
                poem.title = title
                poem.notes = notes
                poem.line_break = ",".join(map(str, line_breaks))
                poem_lines = CurrentUnsavedPoemLines.query.filter_by(
                    user_id=current_user.id)
                # delete any current lines
                if poem_lines.all():
                    poem_lines.delete()
                    db.session.commit()
                # replace with line num from our current unsaved rhymes and text we got in the request
                for i, j in zip(rhyme_check, filtered_req):
                    print(i, j)
                    new_poem_lines = CurrentUnsavedPoemLines(
                        user_id=current_user.id, line_num=i, line_text=j)
                    db.session.add(new_poem_lines)
                    db.session.commit()
                return make_response({"response": "success"})

            # server request save edits =============================================================================================================
            if server_request == "save edits":
                title = req["title"]
                brs = req["line_breaks"]
                notes = req["notes"]
                del req["notes"]
                del req["title"]
                del req["line_breaks"]
                # check if any rhymes are not alphabetical or -
                pattern = re.compile("[a-zA-Z-]")
                if session.get("rs", None) == "Custom":
                    for key in req:
                        if not pattern.match(str(key[0])) or not pattern.match(str(key[0])).group() == str(key[0]) or not len(key) == 2:
                            return make_response({"response": "bad input"})
                # update curr poem title rhymes and brs
                # and delete curr lines if there are any to replace with the new ones
                poem = CurrentUnsavedPoem.query.filter_by(
                    user_id=current_user.id).first()
                poem.title = title
                poem.notes = notes
                poem_lines = CurrentUnsavedPoemLines.query.filter_by(
                    user_id=current_user.id)
                if poem_lines.all():
                    poem_lines.delete()
                    db.session.commit()
                rhymes = []
                ctr = 0
                for key, value in req.items():
                    if value != False:
                        if session.get("rs", None) == "Custom":
                            rhymes.append(key.upper())
                            new_poem_lines = CurrentUnsavedPoemLines(
                                user_id=current_user.id, line_num=key.upper(), line_text=value)
                            db.session.add(new_poem_lines)
                            db.session.commit()
                        else:
                            ctr += 1
                            rhymes.append(ctr)
                            new_poem_lines = CurrentUnsavedPoemLines(
                                user_id=current_user.id, line_num=ctr, line_text=value)
                            db.session.add(new_poem_lines)
                            db.session.commit()
                poem.rhymes = ",".join(map(str, rhymes))
                if brs == "":
                    poem.line_break = 0
                else:
                    poem.line_break = brs
                db.session.commit()
                return make_response({"response": "successful"})

            # server_request DRAFT ===============================================================================================================
            if server_request == "save draft":
                # save initial request since next request will need the same elements since it will be an option in the modal
                print("server_request is save draft")
                print("rquest is", req)
                # make vars global so we don't have to keep sending them in the following requests
                global global_title, global_initial_request, global_poem_num, global_notes
                # delete each entry after saving to the var so they don't interfere with our for loop for adding lines
                global_title = req["title"]
                if not global_title:
                    global_title = "None"
                del req["title"]
                global_notes = req["notes"]
                if not global_notes:
                    global_notes = "None"
                    print("no notes")
                del req["notes"]
                # get user poem num
                if "poem_num" in req:
                    global_poem_num = req["poem_num"]
                    del req["poem_num"]
                else:
                    global_poem_num = Users.query.filter_by(
                        id=current_user.id).first().poem_count
                global_initial_request = req
                print("poem num inside save is", global_poem_num)
                # check if this is a new draft by checking if poem already has entry in db
                existing_draft = Drafts.query.filter_by(
                    user_id=current_user.id, poem_count=global_poem_num).first()
                # if there are no drafts of our current poem make a new one
                if not existing_draft:
                    print("draft doesn t exist")
                    print("title is", global_title)
                    print("gloabl peom num", global_poem_num)
                    current_unsaved_poem = CurrentUnsavedPoem.query.filter_by(
                        user_id=current_user.id).first()
                    line_breaks = current_unsaved_poem.line_break
                    # make sure input is valid by referenicng user's initial rhyme scheme
                    # turn into array since data is stored as (A0,B0,A1,...)
                    rhymes = current_unsaved_poem.rhymes.split(",")
                    print(rhymes)
                    for key, rhyme in zip(global_initial_request, rhymes):
                        if (len(global_initial_request) > len(rhymes)) or rhyme != key:
                            # reject input since it means user has changed keys or added an unwanted value
                            return make_response({"response": "input was altered cannot save"})
                    # save draft to db
                    draft = Drafts(user_id=current_user.id, draft_count=1, poem_count=global_poem_num, rhyme_scheme=current_unsaved_poem.rhyme_scheme,
                                   rhymes=current_unsaved_poem.rhymes, title=global_title, notes=global_notes, line_break=line_breaks, save_date=datetime.now())
                    db.session.add(draft)
                    db.session.commit()
                    # save draft lines to db
                    for key, value in global_initial_request.items():
                        draft_lines = DraftLines(draft_id=Drafts.query.filter_by(
                            user_id=current_user.id, draft_count=1, poem_count=global_poem_num).first().draft_id, line_num=key, line_text=value)
                        db.session.add(draft_lines)
                        db.session.commit()
                    return make_response({"response": "successful", "draft_id": draft.draft_id, "draft_num": draft.draft_count, "poem_num": draft.poem_count}, 200)

                # if a draft exists already return to server to display modal
                else:
                    return make_response({"response": "draft already exists"})

            # make a save of the draft with the same poem number but increasing the draft number each time
            if server_request == "save another draft":
                print("init request", global_initial_request)
                # delete these variables since they will interfere in our for loop for adding lines
                if "draft_num" in global_initial_request and "draft_id" in global_initial_request:
                    del global_initial_request["draft_num"]
                    del global_initial_request["draft_id"]
                # check for invalid input before adding new draft by refercing draft's rhymes
                # get most recent draft
                last_draft = Drafts.query.filter_by(
                    user_id=current_user.id, poem_count=global_poem_num).order_by(Drafts.draft_count.desc()).first()
                # turn rhymes into array since it is stored as (A0,B0,A1,...)
                draft_rhymes = last_draft.rhymes.split(",")
                for key, rhyme in zip(global_initial_request, draft_rhymes):
                    if (len(global_initial_request) > len(draft_rhymes)) or rhyme != key:
                        # reject input since it means user has changed keys or added an unwanted value
                        return make_response({"response": "input was altered cannot save"})
                # increment most recent draft count
                draft_count = last_draft.draft_count+1
                # insert new draft
                new_draft = Drafts(user_id=current_user.id, draft_count=draft_count, poem_count=global_poem_num, rhyme_scheme=last_draft.rhyme_scheme,
                                   rhymes=last_draft.rhymes, title=global_title, notes=global_notes, line_break=last_draft.line_break, save_date=datetime.now())
                db.session.add(new_draft)
                db.session.commit()
                # insert draft lines making sure no new lines were added
                for key, value in global_initial_request.items():
                    new_draft_lines = DraftLines(draft_id=Drafts.query.filter_by(
                        user_id=current_user.id, draft_count=draft_count, poem_count=global_poem_num).first().draft_id, line_num=key, line_text=value)
                    db.session.add(new_draft_lines)
                    db.session.commit()
                return make_response({"response": "successful"}, 200)

            # update the draft the user is in currently
            if server_request == "update draft":
                if "draft_num" in global_initial_request:
                    del global_initial_request["draft_num"]
                print("intial req", global_initial_request, "\ntitle inside update is", global_title,
                      "\npoemnum", global_poem_num, "\ndraft_id in req", "draft_id" in global_initial_request)
                if "draft_id" in global_initial_request:
                    draft_to_update = Drafts.query.filter_by(
                        user_id=current_user.id, draft_id=global_initial_request["draft_id"]).first()
                    del global_initial_request["draft_id"]
                else:
                    draft_to_update = Drafts.query.filter_by(
                        user_id=current_user.id, poem_count=global_poem_num).order_by(Drafts.draft_count.desc()).first()
                # check for invalid input by referencing original rhymes when poem was created before updating draft
                draft_to_update = Drafts.query.filter_by(
                    user_id=current_user.id, draft_count=draft_to_update.draft_count, poem_count=global_poem_num).first()
                # turn rhymes into array since it is stored as (A0,B0,A1,...)
                rhymes = draft_to_update.rhymes.split(",")
                for key, rhyme in zip(global_initial_request, rhymes):
                    if (len(global_initial_request) > len(rhymes)) or rhyme != key:
                        # reject input since it means user has changed keys or added an unwanted value
                        return make_response({"response": "input was altered cannot save"})
                # update current draft
                draft_to_update.title = global_title
                draft_to_update.notes = global_notes
                draft_to_update.edit_date = datetime.now()
                draft_to_update.saved = 0
                db.session.commit()
                # update draft and lines
                for key, value in global_initial_request.items():
                    draft_lines_to_update = DraftLines.query.filter_by(
                        draft_id=draft_to_update.draft_id, line_num=key).first()
                    draft_lines_to_update.line_text = value
                    db.session.commit()
                return make_response({"response": "successful"}, 200)

            # does not share global initial request with other server_Requests!
            # REQUEST Save poem ============================================================================================================
            if server_request == "save poem":
                print("save poem", req)
                poem_title = req["title"]
                del req["title"]
                # add saved state to draft
                if req["draft_id"] == None:
                    draft = CurrentUnsavedPoem.query.filter_by(
                        user_id=current_user.id)
                else:
                    draft = Drafts.query.filter_by(
                        user_id=current_user.id, draft_id=req["draft_id"])
                del req["draft_id"]
                ctr = 0
                # turn rhymes into array since it is stored as (A0,B0,A1,...)
                rhymes = draft.first().rhymes.split(",")
                for key, value in req.items():
                    if (ctr > len(rhymes)) or rhymes[ctr] != key:
                        # reject input since it means user has changed keys or added an unwanted value
                        return make_response({"response": "input was altered cannot save"})
                    ctr += 1
                # mark draft as saved
                draft.first().saved = 1
                # increment user saved poem count
                current_user.saved_poem_count += 1
                db.session.commit()
                line_breaks = CurrentUnsavedPoem.query.filter_by(
                    user_id=current_user.id).first().line_break
                # add poem to db
                user_poem = Poems(user_id=current_user.id, poem_count=current_user.saved_poem_count, rhyme_scheme=draft.first(
                ).rhyme_scheme, title=poem_title, line_break=line_breaks, rhymes=draft.first().rhymes, save_date=datetime.now())
                db.session.add(user_poem)
                db.session.commit()

                for key, value in req.items():
                    # add checking if lines no matching
                    user_poem_lines = PoemLines(poem_id=Poems.query.filter_by(
                        user_id=current_user.id, poem_count=current_user.saved_poem_count).first().poem_id, line_num=key, line_text=value)
                    db.session.add(user_poem_lines)
                    db.session.commit()
                if request.cookies.get("del_draft") == "True":
                    draft.delete()
                    db.session.commit()
                return make_response({"response": "successful"})
            # does not share global initial request with other server_Requests!
            # REQUEST UPDATE POEM====================================================================================================================================================================================
            if server_request == "update poem":
                title = req["title"]
                updated_poem = Poems.query.filter_by(
                    user_id=current_user.id, poem_id=req["poem_id"]).first()
                del req["title"]
                del req["poem_id"]
                rhymes = updated_poem.rhymes.split(",")
                for key, rhyme in zip(req, rhymes):
                    if (len(req) > len(rhymes)) or rhyme != key:
                        # reject input since it means user has changed keys or added an unwanted value
                        return make_response({"response": "input was altered cannot save"})
                    ctr += 1
                updated_poem.title = title
                updated_poem.edit_date = datetime.now()
                for key, value in req.items():
                    updated_poem_lines = PoemLines.query.filter_by(
                        poem_id=updated_poem.poem_id, line_num=key).first()
                    updated_poem_lines.line_text = value
                db.session.commit()
                return make_response({"response": "successful"}, 200)


@app.route("/Meter")
def meter():
    return render_template("meter.html")


@app.route("/Format", methods=["POST", "GET"])
@login_required
def format():
    if request.method == "GET":
        user_poem = Poems.query.filter_by(user_id=current_user.id, poem_count=Users.query.filter_by(
            id=current_user.id).first().saved_poem_count).first()
        user_poem_lines = PoemLines.query.filter_by(
            poem_id=user_poem.poem_id).all()
        return render_template("format.html", user_poem=user_poem, user_poem_lines=user_poem_lines, username=current_user.username)
    if request.method == "POST":
        req = request.get_json()
        if request.headers["Request"] == "save poem":
            print("req is", req)
            user_poem = Poems.query.filter_by(user_id=current_user.id, poem_count=Users.query.filter_by(
                id=current_user.id).first().saved_poem_count).first()
            user_poem.title = user_poem.title
            # add lines to db
            for key, value in req.items():
                user_poem_lines = PoemLines.query.filter_by(
                    poem_id=user_poem.poem_id, line_num=key).first()
                user_poem_lines.line_text = value
                db.session.commit()
            return make_response({"response": "successful"})


# take user queries and return corresponding result from datamuse API
@app.route("/Rhymes", methods=["POST", "GET"])
def rhymes():
    form = RhymesForm()
    if request.method == "GET":
        if request.args.get("query") and request.args.get("filters"):
            query = request.args.get("query")
            user_filters = request.args.get("filters")
            # repopulate the form with user's inputs
            form.query.data = query
            form.filters.data = user_filters
            url = f"https://api.datamuse.com/words?{user_filters}={query}&max=1000&md=d"
            datamuse_api_response = requests.get(url)
            datamuse_api_response = datamuse_api_response.json()
            # if we get no results back
            if len(datamuse_api_response) == 0:
                return render_template("rhymes.html", form=form, no_results="There are no words that match your search")
            # if the user is looking for a rhyme filter the response into an array of objects
            # with the syllable num as the key and an object of the word and the word and it's definition as the value
            # obj = [{numsyllables:{word:def}}, {numsyllables:{word:def}}, ....]
            if user_filters == "rel_rhy":
                syllables = []
                resp_obj = {}
                for i in datamuse_api_response:
                    if i["numSyllables"] not in syllables:
                        syllables.append(i["numSyllables"])
                for i in syllables:
                    resp_obj[i] = []
                    for j in datamuse_api_response:
                        if i == j["numSyllables"]:
                            if "defs" in j:
                                resp_obj[i].append({j["word"]: j["defs"]})
                            else:
                                resp_obj[i].append({j["word"]: "None"})
                return render_template("rhymes.html", form=form, resp=dict(sorted(resp_obj.items())))
            return render_template("rhymes.html", form=form, resp=datamuse_api_response)
        return render_template("rhymes.html", form=form)
    if request.method == "POST":
        # to check if 2 words rhyme
        if "Request" in request.headers and request.headers["Request"] == "check if words rhyme":
            req = request.get_json()
            return make_response({"response": isRhyme(req["request"][0], req["request"][1], 1)})


# display full definitions for reulst
@app.route("/Rhymes/Definition")
def rhymes_def():
    initial_word = request.args.get("i")
    filter = request.args.get("f")
    url = f"https://api.datamuse.com/words?{filter}={initial_word}&max=1000&md=d"
    print(url)
    resp = requests.get(url)
    word = request.args.get("word")
    for i in resp.json():
        if i["word"] == word:
            if "defs" in i:
                definition = i["defs"]
                break
            else:
                return render_template("rhymes_def.html", no_results=f'"{word}" has no known definitions in our dictionary')
    if len(definition) == 0:
        return render_template("rhymes_def.html", no_results=f'"{word}" has no known definitions in our dictionary')
    def_obj = {"Noun": [], "Verb": [],
               "Adjective": [], "Adverb": [], "Undefined": []}
    for i in definition:
        if i[0] == "n":
            def_obj["Noun"].append(i[1:])
        elif i[0] == "v":
            def_obj["Verb"].append(i[1:])
        elif i[0] == "u":
            def_obj["Unidentified"].append(i[1:])
        elif i[0:3] == "adj":
            def_obj["Adjective"].append(i[3:])
        elif i[0:3] == "adv":
            def_obj["Adverb"].append(i[3:])
        # switch statements had to be commented out to work with render.com
        # match i[0]:
        #     case "n":
        #         def_obj["Noun"].append(i[1:])
        #     case "v":
        #         def_obj["Verb"].append(i[1:])
        #     case "u":
        #         def_obj["Unidentified"].append(i[1:])
        # match i[0:3]:
        #     case "adj":
        #         def_obj["Adjective"].append(i[3:])
        #     case "adv":
        #         def_obj["Adverb"].append(i[3:])
    print(def_obj)

    return render_template("rhymes_def.html", definition=def_obj, word=word)


# take user queries and return corresponding result from poetrydb API
@app.route("/SearchPoems", methods=["POST", "GET"])
def search_poems():
    form = SearchPoemsForm(request.args)
    if request.method == "GET":
        # random query
        if request.args.get("poem_rand"):
            # get response from api
            url = "https://poetrydb.org/random/20"
            poetrydb_api_response = requests.get(url)
            poetrydb_api_response = poetrydb_api_response.json()
            # setup for pagination
            page = int(request.args.get('page', 1))
            per_page = 20
            offset = (page - 1) * per_page
            items_pagination = poetrydb_api_response[offset:offset+per_page]
            total = len(poetrydb_api_response)
            pagination = Pagination(
                page=page, per_page=per_page, offset=offset, total=total)
            return render_template("search_poems.html", form=form, poetrydb_api_response=poetrydb_api_response, pagination=pagination, items=items_pagination, poem_rand=True)
        # normal query
        elif request.args.get("query") and request.args.get("filters"):
            # refill the form with the user's input
            form.query.data = request.args.get("query")
            form.filters.data = request.args.get("filters")
            query = form.query.data.strip().replace(" ", "%20")

            # if user specified poem_length
            if (request.args.get("poem_length")):
                url = f"https://poetrydb.org/{form.filters.data},linecount/{query};{request.args.get('poem_length')}"
            else:
                url = f"https://poetrydb.org/{form.filters.data}/{query}"
            poetrydb_api_response = requests.get(url)
            print(poetrydb_api_response)
            poetrydb_api_response = poetrydb_api_response.json()
            # if user has a min and max lincount filter modify enteries
            if (request.args.get("min_length")):
                min_len = request.args.get("min_length")
                poetrydb_api_response = [
                    i for i in poetrydb_api_response if int(i["linecount"]) > int(min_len)]
            if (request.args.get("max_length")):
                max_len = request.args.get("max_length")
                poetrydb_api_response = [
                    i for i in poetrydb_api_response if int(i["linecount"]) < int(max_len)]

            # if user wants to sort results sort accordingly
            if (request.args.get("sort_by")):
                form.sort_by.data = request.args.get("sort_by")
                if request.args.get("sort_by") == "shortest":
                    poetrydb_api_response.sort(
                        key=lambda i: int(i["linecount"]))
                elif request.args.get("sort_by") == "longest":
                    poetrydb_api_response.sort(
                        key=lambda i: int(i["linecount"]), reverse=True)
                elif request.args.get("sort_by") == "author":
                    poetrydb_api_response.sort(key=lambda i: i["author"])
                elif request.args.get("sort_by") == "author_reverse":
                    poetrydb_api_response.sort(
                        key=lambda i: i["author"], reverse=True)
                elif request.args.get("sort_by") == "title":
                    poetrydb_api_response.sort(key=lambda i: i["title"])
                elif request.args.get("sort_by") == "title_reverse":
                    poetrydb_api_response.sort(
                        key=lambda i: i["title"], reverse=True)

                # match request.args.get("sort_by"):
                #     case "shortest":
                #         poetrydb_api_response.sort(key=lambda i: int(i["linecount"]))
                #     case "longest":
                #         poetrydb_api_response.sort(key=lambda i: int(i["linecount"]), reverse=True)
                #     case "author":
                #         poetrydb_api_response.sort(key=lambda i: i["author"])
                #     case "author_reverse":
                #         poetrydb_api_response.sort(key=lambda i: i["author"], reverse=True)
                #     case "title":
                #         poetrydb_api_response.sort(key=lambda i: i["title"])
                #     case "title_reverse":
                #         poetrydb_api_response.sort(key=lambda i: i["title"], reverse=True)
            # if no results match user's search
            if "status" in poetrydb_api_response and poetrydb_api_response["status"] == 404:
                return render_template("search_poems.html", form=form, not_found="There are no results that match your search check your spelling or try again")
            # if there is a response
            if len(poetrydb_api_response) != 0:
                page = int(request.args.get('page', 1))
                per_page = 20
                offset = (page - 1) * per_page
                items_pagination = poetrydb_api_response[offset:offset+per_page]
                total = len(poetrydb_api_response)
                pagination = Pagination(
                    page=page, per_page=per_page, offset=offset, total=total)
                return render_template("search_poems.html", form=form, pagination=pagination, items=items_pagination)
            # if there's no response
            return render_template("search_poems.html", form=form, not_found="There are no results that match your search")
        # if there is no query url parameter
        else:
            return render_template("search_poems.html", form=form)
    if request.method == "POST":
        # if an ajax request is sent
        if "Request" in request.headers:
            # randomise results
            if request.headers["Request"] == "randomise":
                return make_response({"response": "success"})


# displays poem on whole page
@app.route("/SearchPoems/<string:author>/<string:title>")
def search_poems_display(author, title):
    url = f"https://poetrydb.org/author,title/{author.replace(' ','%20')};{title.replace(' ','%20')};"
    poem = requests.get(url)
    return render_template("search_poems_display.html", poem=poem.json())


# Account dropdown

@app.route("/Account/Settings", methods=["POST", "GET"])
@login_required
def settings():
    form = SettingsForm()
    if request.method == "GET":
        print("cookies", request.cookies.get('detatch_util'))
        detatch_util = request.cookies.get('detatch_util')
        hide_detatch_btn = request.cookies.get("hide_detatch_btn")
        disable_reminder = request.cookies.get("disable_reminder")
        del_draft = request.cookies.get("del_draft")
        return render_template("settings.html", form=form, detatch_util=detatch_util, hide_detatch_btn=hide_detatch_btn, disable_reminder=disable_reminder, del_draft=del_draft)
    if request.method == "POST":
        if "Request" in request.headers and request.headers["Request"] == "change username":
            req = request.get_json()
            pattern = re.compile("^[A-Za-z][A-Za-z0-9_]{2,29}$")
            username = req["request"]
            if pattern.match(str(username)) and pattern.match(str(username)).group() == str(username):
                current_user.username = username
                db.session.commit()
                return make_response({"response": "successful"})
            else:
                return make_response({"response": "invalid username"})
        resp = make_response(redirect(url_for("settings")))
        resp.set_cookie("detatch_util", value=str(
            form.detatch_util.data),  expires=datetime.now() + timedelta(days=365))
        resp.set_cookie("hide_detatch_btn", value=str(
            form.hide_detatch_btn.data),  expires=datetime.now() + timedelta(days=365))
        resp.set_cookie("disable_reminder", value=str(
            form.disable_reminder.data),  expires=datetime.now() + timedelta(days=365))
        resp.set_cookie("del_draft", value=str(form.del_draft.data),
                        expires=datetime.now() + timedelta(days=365))
        return resp


@app.route("/Account/Draft", methods=["POST", "GET"])
@login_required
def drafts():
    if request.method == "GET":
        drafts = Drafts.query.filter_by(user_id=current_user.id).order_by(
            Drafts.poem_count.asc()).all()
        draft_lines = DraftLines.query.all()
        del_draft = request.cookies.get("del_draft")
        return render_template("drafts-poems.html", user_poems=drafts, poem_lines=draft_lines, del_draft=del_draft, session="draft")
    if request.method == "POST":
        req = request.get_json()
        print("req is", req)
        if "Request" in request.headers and request.headers["Request"] == "delete draft":
            draft = Drafts.query.filter_by(
                user_id=current_user.id, draft_id=req["draft_id"])
            draft_num = draft.first().draft_count
            poem_num = draft.first().poem_count
            draft_title = draft.first().title
            DraftLines.query.filter_by(
                draft_id=draft.first().draft_id).delete()
            draft.delete()
            db.session.commit()
            return {"response": "Draft Deleted", "draft_title": draft_title, "draft_num": draft_num, "poem_num": poem_num}


@app.route("/Account/Draft/Display")
@login_required
def display_draft():
    draft = Drafts.query.filter_by(
        user_id=current_user.id, draft_id=request.args.get("pid")).first()
    draft_lines = DraftLines.query.filter_by(draft_id=draft.draft_id).all()
    return render_template("draft-poem_display.html", poem=draft, poem_lines=draft_lines, session="draft")


@app.route("/Account/Poems", methods=["POST", "GET"])
@login_required
def poems():
    if request.method == "GET":
        user_poems = Poems.query.filter_by(user_id=current_user.id).all()
        poem_lines = PoemLines.query.all()
        return render_template("drafts-poems.html", user_poems=user_poems, poem_lines=poem_lines, username=current_user.username, session="poem")
    if request.method == "POST":
        req = request.get_json()
        if request.headers["Request"] == "delete poem":
            poem_id = req["poem_id"]
            poem = Poems.query.filter_by(
                user_id=current_user.id, poem_id=poem_id)
            poem_title = poem.first().title
            poem_num = poem.first().poem_count
            PoemLines.query.filter_by(poem_id=poem.first().poem_id).delete()
            poem.delete()
            db.session.commit()
            return make_response({"response": "successful", "poem_title": poem_title, "poem_num": poem_num})


@app.route("/Account/Poem/Display")
@login_required
def display_poem():
    poem = Poems.query.filter_by(
        user_id=current_user.id, poem_id=request.args.get("pid")).first()
    poem_lines = PoemLines.query.filter_by(poem_id=poem.poem_id).all()
    return render_template("draft-poem_display.html", poem=poem, poem_lines=poem_lines, session="poem")
