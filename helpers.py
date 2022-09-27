from encodings import normalize_encoding
import os
import urllib.parse
import urllib.request
import json
import sys
import sqlite3

from flask import redirect, request, session, g
from functools import wraps
from app import app

# require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/Signin")
        return f(*args, **kwargs)
    return decorated_function

# Configure db
DATABASE = "database.db"

def get_db():

    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#configure file uploads
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', "png"}
app.config['MAX_CONTENT_LENGTH'] = 8 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# rhyming fucntions
# def rhymes(word1, word2):
#     url = ("https://api.datamuse.com/words?rel_rhy="+word2)
#     response = urllib.request.urlopen(url)
#     data = response.read()
#     rhymes_dict = json.loads(data)
#     for i in rhymes_dict:
#         if word1 == i["word"]:
#             return True
#     return False

# def near_rhymes(word1, word2):
#     url = ("https://api.datamuse.com/words?rel_nry="+word2)
#     response = urllib.request.urlopen(url)
#     data = response.read()
#     near_rhymes_dict = json.loads(data)
#     for i in near_rhymes_dict:
#         if word1 == i["word"]:
#             return True
#     return False


# rhyming functions
json_entries = None

def tup2dict(tup, di):
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di
# initiate dict
def init_cmu():
    import nltk
    nltk.download('cmudict')
    print(nltk.download('cmudict'))
    nltk.corpus.cmudict.ensure_loaded()
    print(nltk.corpus.cmudict.ensure_loaded())
    cmu_entries = nltk.corpus.cmudict.entries()
    # print(cmu_entries)
    cmu_dict = dict()
    print(cmu_dict)
    tup2dict(cmu_entries, cmu_dict)
    # print(cmu_dict)
    with open('C:/Users/user/AppData/Roaming/nltk_data/corpora/cmudict.json', 'w') as convert_file:
        convert_file.write(json.dumps(cmu_dict))

def require_rhyme_dict():
    global json_entries
    if json_entries:
        return
    try:
        jsonf = open('C:/Users/user/AppData/Roaming/nltk_data/corpora/cmudict.json', 'r')
    except:
        print("file unable to be opened")
    else:
        # Global
        json_entries = dict(json.load(jsonf))
        jsonf.close()
        print('file opened and json_entries loaded.')

def isRhyme(word1, word2, level):
    require_rhyme_dict()
    global json_entries
    word1_syllable_arrs = json_entries.get(word1)
    word2_syllables_arrs = json_entries.get(word2)
    if not word1_syllable_arrs or not word2_syllables_arrs:
        return False
    for a in word1_syllable_arrs:
        for b in word2_syllables_arrs:
            if a[-level:] == b[-level:]:
                return True
    return False

# syllable functions
def lookup_word(word_s):
    require_rhyme_dict()
    global json_entries
    return json_entries.get(word_s)

def count_syllables(word_s):
    require_rhyme_dict()
    global json_entries
    count = 0
    phones = lookup_word(word_s) 
    if phones:                   
        phones0 = phones[0]      
        count = len([p for p in phones0 if p[-1].isdigit()]) 
    return count

# repeat a given pattern x amount of times by changing the elements example ["A","B"] repeat 2 change by 1 ["A","B","B","C","C","D"]
def repeat_pattern(pattern, change_by, repeats, envoi):
    print("repeat call")
    if change_by == None and repeats == None:
        return pattern
    temp_pattern = []
    return_pattern_arr = []
    for i in pattern:
        temp_pattern.append(ord(i))
    temp_pattern_len = len(temp_pattern)
    ctr = change_by
    for i in range(int(repeats)+1):
        if i>1 and change_by!=0:
            ctr+=change_by
        for j in range(temp_pattern_len):
            if i!=0:
                temp_pattern.append(temp_pattern[j]+ctr)
    for i in range(len(temp_pattern)):
        return_pattern_arr.append(chr(temp_pattern[i]))
    if envoi != None:
        for i in envoi:
            return_pattern_arr.append(i)
    return return_pattern_arr

# converst ["A","B","A"] to ["A0","B0","A1"]
def get_id(letter_array):
    print("get id call")
    letters = {}
    return_arr = []
    for i in range(len(letter_array)):
        if letter_array[i] not in letters:
            letters[letter_array[i]] = 0
            return_arr.append(letter_array[i]+str(0))
        else:
            letters[letter_array[i]]+=1
            return_arr.append(letter_array[i]+str(letters[letter_array[i]]))
    return return_arr

# returns which lines to add a break after ["A4","B3"]....
def get_line_breaks(arr,frequency):
    line_breaks = []
    if not frequency or frequency == None:
        return
    for i in range(len(arr)):
        if i%int(frequency) == 0 and i!=0:
            line_breaks.append(arr[i-1])
    return line_breaks

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

# obj used in  /Create /write
rhyme_schemes = [
                 "Monorhyme", 
                 "Coupled Rhyme", 
                 "Triplet",
                 "Alternating Rhyme", 
                 "Encolsed Rhyme", 
                 "Free Verse",
                 "Custom",
                 "Fixed Rhyme Schemes...",
                 "Shakespearean Sonnet",
                 "Terza Rima",
                 "Limerick",
                 "Haiku"
                 ]

FIXED_RHYME_SCHEMES = ["Limerick","Shakespearean Sonnet","Haiku","Free Verse","Custom","Terza Rima", "Vilanelle"]
CUSTOM_BR = ["Monorhyme", "Free Verse", "Custom"]

# Classes
class rhyme_scheme:
    def __init__(self, _name, _rhymes, _repeats, _increment_by, _envoi, _line_break_frequency):
        self.name = _name
        self.rhymes = _rhymes
        self.repeats = _repeats
        self.increment_by = _increment_by
        self.envoi = _envoi
        self.line_break_frequency = _line_break_frequency
    def get_ids(self):
        print("class func get ids call")
        print("repeats and increments and rhymes",self.repeats, self.increment_by, self.rhymes)
        temp = 0
        # repeat pattern func defined above but cannot use inside object function or it will result in multiple calls of the function for each letter
        if self.repeats == None and self.increment_by == None:
            temp = self.rhymes
        else:
            print("else")
            temp_pattern = []
            return_pattern_arr = []
            for i in self.rhymes:
                temp_pattern.append(ord(i))
            temp_pattern_len = len(temp_pattern)
            ctr = self.increment_by
            for i in range(int(self.repeats)+1):
                if i>1 and self.increment_by!=0:
                    ctr+=self.increment_by
                for j in range(temp_pattern_len):
                    if i!=0:
                        temp_pattern.append(temp_pattern[j]+ctr)
            for i in range(len(temp_pattern)):
                return_pattern_arr.append(chr(temp_pattern[i]))
            if self.envoi != None:
                for i in self.envoi:
                    return_pattern_arr.append(i)
            temp = return_pattern_arr
        # get ids func defined above
        letters = {}
        return_arr = []
        for i in range(len(temp)):
            if temp[i] not in letters:
                letters[temp[i]] = 0
                return_arr.append(temp[i]+str(0))
            else:
                letters[temp[i]]+=1
                return_arr.append(temp[i]+str(letters[temp[i]]))
        # store value in obj to not call the func again inside get_br
        return return_arr
        

Monorhyme = rhyme_scheme("Monorhyme", ["A"], 1, 0,None, None) 
Coupled_Rhyme = rhyme_scheme("Coupled Rhyme",["A","A"], 1, 1, None, 2)
Triplet = rhyme_scheme("Triplet", ["A","A","A"], 1, 1, None, 3)
Alternating_Rhyme = rhyme_scheme("Alternating Rhyme", ["A","B","A","B"], 1, 2,None, 4)
Encolsed_Rhyme = rhyme_scheme("Encolsed Rhyme", ["A","B","B","A"], 1, 2, None, 4)
Free_Verse = rhyme_scheme("Free Verse", [], None, None, None, None)
Custom = rhyme_scheme("Custom", [], None, None, None, None)
Shakespearean_Sonnet = rhyme_scheme("Shakespearean Sonnet", ["A","B","A","B"], 2, 2, ["G","G"], 4)
Terza_Rima = rhyme_scheme("Terza_Rima", ["A","B","A"], 3, 1, ["E","E"], 3)
Limerick = rhyme_scheme("Limerick", ["A","A","B","B","A"], None, None, None, None)
Haiku = rhyme_scheme("Haiku", ["1","2","3"], None, None, None, None)




class draft:
        def __init__(self,_poem_draft, _poem_num, _draft_num):
            self.poem_draft = _poem_draft
            self.poem_num = _poem_num
            self.draft_num = _draft_num
            self.rhymes = None
        def get_title(self):
            row = query_db("SELECT * FROM draft WHERE user_id = ? AND poem_num = ? AND draft_num =?", 
            [session.get("user_id", None), self.poem_num, self.draft_num], one=True)
            return row["title"]
        def get_lines(self):
            print("get lines call")
            line_obj = {}
            db=get_db()
            cur = db.cursor()
            cur.execute("SELECT line_num, line_text FROM draft WHERE user_id = ? AND poem_num = ? AND draft_num =?", 
            (session.get("user_id", None), self.poem_num, self.draft_num))
            for i in cur:
                line_obj[i["line_num"]]= i["line_text"]
            cur.close()
            self.rhymes = line_obj
            return line_obj
        def get_rhyme_scheme(self):
            row = query_db("SELECT * FROM draft WHERE user_id = ? AND poem_num = ? AND draft_num =?", 
            [session.get("user_id", None), self.poem_num, self.draft_num], one=True)
            return row["rhyme_scheme"]
        def get_time(self):
            row = query_db("SELECT * FROM draft WHERE user_id = ? AND poem_num = ? AND draft_num =?", 
            [session.get("user_id", None), self.poem_num, self.draft_num], one=True)
            return row["date"]
        def get_notes(self):
            row = query_db("SELECT * FROM draft WHERE user_id = ? AND poem_num = ? AND draft_num =?", 
            [session.get("user_id", None), self.poem_num, self.draft_num], one=True)
            return row["notes"]
        def get_line_breaks(self):
            row = query_db("SELECT * FROM draft WHERE user_id = ? AND poem_num = ? AND draft_num =?", 
            [session.get("user_id", None), self.poem_num, self.draft_num], one=True)
            return row["line_breaks"]

class poem:
    def __init__(self, _poem_id):
        self.poem_id = _poem_id
    def get_title(self):
        row = query_db("SELECT * FROM poem WHERE user_id = ? AND poem_id = ?", 
        [session.get("user_id", None), self.poem_id], one=True)
        return row["title"]
    def get_lines(self):
        line_obj = {}
        db=get_db()
        cur = db.cursor()
        cur.execute("SELECT line_num, line_text FROM poem WHERE user_id = ? AND poem_id = ?", 
        (session.get("user_id", None), self.poem_id))
        for i in cur:
            line_obj[i["line_num"]]= i["line_text"]
        cur.close()
        return line_obj
    def get_rhyme_scheme(self):
        row = query_db("SELECT * FROM poem WHERE user_id = ? AND poem_id =?", 
            [session.get("user_id", None), self.poem_id], one=True)
        return row["rhyme_scheme"]
    def get_line_breaks(self):
        row = query_db("SELECT * FROM poem WHERE user_id = ? AND poem_id =?", 
            [session.get("user_id", None), self.poem_id], one=True)
        return row["line_breaks"]
    def get_poem_num(self):
        row = query_db("SELECT * FROM poem WHERE user_id = ? AND poem_id =?", 
            [session.get("user_id", None), self.poem_id], one=True)
        return row["poem_num"]
    def get_time(self):
        row = query_db("SELECT * FROM poem WHERE user_id = ? AND poem_id =?", 
            [session.get("user_id", None), self.poem_id], one=True)
        return row["date"]