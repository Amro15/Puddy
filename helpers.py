# import os
# import urllib.request
# import sqlite3
from urllib.parse import urlparse, urljoin
import json
import sys
import re
from flask import request #,session, g,redirect,
# from functools import wraps
from app import app
# import prosodic as p

# def check_meter(sentence):
#     temp = []
#     text = p.Text(sentence)
#     text.parse()
#     for parse in text.bestParses():
#         temp.append(parse)
#     return temp

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

#configure file uploads
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', "png"}
app.config['MAX_CONTENT_LENGTH'] = 8 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# rhyming functions
json_entries = None

def tup2dict(tup, di):
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di
    
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

regex = r'[0-9]'
def isRhyme(word1, word2, level):
    require_rhyme_dict()
    global json_entries
    word1_syllable_arrs = json_entries.get(word1)
    word2_syllables_arrs = json_entries.get(word2)
    if not word1_syllable_arrs or not word2_syllables_arrs:
        return False
    for a in word1_syllable_arrs:
        for b in word2_syllables_arrs:
            # if a[-level:] == b[-level:]:
            if re.sub(regex,"",a[-level]) == re.sub(regex,"",b[-level]):
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



# obj used in  /Create /write
rhyme_schemes = [
                 "Monorhyme", 
                 "Coupled Rhyme", 
                 "Triplet",
                 "Alternating Rhyme", 
                 "Encolsed Rhyme", 
                 "Blank Verse",
                 "Free Verse",
                 "Custom",
                 "Fixed Rhyme Schemes...",
                 "Shakespearean Sonnet",
                 "Terza Rima",
                 "Limerick",
                 "Haiku"
                 ]

CUSTOM_BR = ["Monorhyme", "Free Verse", "Custom"]

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
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
        print("repeats and increments and rhymes",self.repeats, self.increment_by, self.rhymes)
        temp = 0
        # repeat pattern func present at bottom of page but cannot use inside object function or it will result with the function being called once for for each letter
        if self.repeats == None and self.increment_by == None:
            temp = self.rhymes
        else:
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
        # get ids func defined below
        letters = {}
        return_arr = []
        for i in range(len(temp)):
            if isinstance(temp[0], int):
                return temp
            if temp[i] not in letters:
                letters[temp[i]] = 0
                return_arr.append(temp[i]+str(0))
            else:
                letters[temp[i]]+=1
                return_arr.append(temp[i]+str(letters[temp[i]]))
        # store value in obj to not call the func again inside get_br
        return return_arr
        
# name, rhymes, repeats, increment_by, envoi, line_break_frequency
Monorhyme = rhyme_scheme("Monorhyme", ["A"], 0, 0,None, None) 
Coupled_Rhyme = rhyme_scheme("Coupled Rhyme",["A","A"], 0, 1, None, 2)
Triplet = rhyme_scheme("Triplet", ["A","A","A"], 0, 1, None, 3)
Alternating_Rhyme = rhyme_scheme("Alternating Rhyme", ["A","B","A","B"], 0, 2,None, 4)
Encolsed_Rhyme = rhyme_scheme("Encolsed Rhyme", ["A","B","B","A"], 0, 2, None, 4)
Free_Verse = rhyme_scheme("Free Verse", [], None, None, None, None)
Blank_Verse = rhyme_scheme("Blank Verse", [], None, None, None, None)
Custom = rhyme_scheme("Custom", [], None, None, None, None)
Shakespearean_Sonnet = rhyme_scheme("Shakespearean Sonnet", ["A","B","A","B"], 2, 2, ["G","G"], 4)
Terza_Rima = rhyme_scheme("Terza Rima", ["A","B","A"], 3, 1, ["E","E"], 3)
Limerick = rhyme_scheme("Limerick", ["A","A","B","B","A"], None, None, None, None)
Haiku = rhyme_scheme("Haiku", ["1","2","3"], None, None, None, None)


# # repeat a given pattern x amount of times by changing the elements example ["A","B"] repeat 2 change by 1 ["A","B","B","C","C","D"]
# def repeat_pattern(pattern, change_by, repeats, envoi):
#     print("repeat call")
#     if change_by == None and repeats == None:
#         return pattern
#     temp_pattern = []
#     return_pattern_arr = []
#     for i in pattern:
#         temp_pattern.append(ord(i))
#     temp_pattern_len = len(temp_pattern)
#     ctr = change_by
#     for i in range(int(repeats)+1):
#         if i>1 and change_by!=0:
#             ctr+=change_by
#         for j in range(temp_pattern_len):
#             if i!=0:
#                 temp_pattern.append(temp_pattern[j]+ctr)
#     for i in range(len(temp_pattern)):
#         return_pattern_arr.append(chr(temp_pattern[i]))
#     if envoi != None:
#         for i in envoi:
#             return_pattern_arr.append(i)
#     return return_pattern_arr

# # converst ["A","B","A"] to ["A0","B0","A1"]
# def get_id(letter_array):
#     print("get id call")
#     letters = {}
#     return_arr = []
#     for i in range(len(letter_array)):
#         if letter_array[i] not in letters:
#             letters[letter_array[i]] = 0
#             return_arr.append(letter_array[i]+str(0))
#         else:
#             letters[letter_array[i]]+=1
#             return_arr.append(letter_array[i]+str(letters[letter_array[i]]))
#     return return_arr