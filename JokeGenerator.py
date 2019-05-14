import os
import random
import json
import Net
import hashlib

class JokeGenerator:
    def __init__(self,joke_db):
        self.db_filename = joke_db
        self.db = {}
        self.replacement_dict = {}
        self.net_success = False
        try:
            self.db = json.load(open(joke_db,'r'))
        except:
            self.db["old"] = []
            self.db["new"] = []
            self.save_db()
        try:
            self.replacement_dict = json.load(open("politically_correct.json",'r'))
        except:
            self.replacement_dict["black"] = ["white"]
            self.replacement_dict["jew"] = ["[REDACTED]"]
            self.replacement_dict["holocaust"]  = ["great leap forward"]
            self.replacement_dict["nigger"] = ["cracker"]
    
    def save_db(self):
        json.dump(self.db, open(self.db_filename,"w"))

    def get_joke(self):
        if(len(self.db["new"]) <= 0):
            self.generate_new()
        joke = self.db["new"].pop(0)
        if(self.net_success):
            self.db["old"].append(hash(joke))
        self.save_db()
        return joke

    def make_PC(self,text):
        words = text.split(" ")
        ret = ""
        for word in words:
            comp_word = word.lower()
            comp_word = self.remove_all_but(comp_word,"abcdefghijklmnopqrstuvwxyz")
            if(comp_word in self.replacement_dict):
                w = random.choice(self.replacement_dict[comp_word])
                ret += w + " "
            else:
                ret += word + " "
        return ret
        
    def remove_all_but(self,text,allowed):
        ret = ""
        for c in text:
            if(c in allowed):
                ret += c
        return ret

    def generate_new(self):
        raw_str = ""
        self.net_success = True
        try:
            raw_str = Net.run(2000) #runs the net for 2000 characters
            self.net_success = True
        except:        
            raw_str = " \nthis is a test. jokebot will start producing jokes soon.\n "
            self.net_success = False
        ret = raw_str.split("\n")
        if(len(ret) > 2):
            for new_joke in ret[1:-1]:
                new_joke_pc = self.make_PC(new_joke)
                h = hash(new_joke_pc)
                if not h in self.db["old"]: 
                    self.db["new"].append(new_joke_pc)
        else:
            self.db["new"] = ["Couldn't get any jokes from my stupid neural network, it did produce something but it's crap"]   
            self.net_success = False
        
