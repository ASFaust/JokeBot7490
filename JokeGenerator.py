import os
import random
import json
import Net
import hashlib

class JokeGenerator:
    def __init__(self,joke_db):
        self.db_filename = joke_db
        self.db = {}
        try:
            self.db = json.load(open(joke_db,'r'))
        except:
            self.db["old"] = []
            self.db["new"] = []
            self.save_db()
    
    def save_db(self):
        json.dump(self.db, open(self.db_filename,"w"))

    def get_joke(self):
        if(len(self.db["new"]) <= 0):
            self.generate_new()
        joke = self.db["new"].pop(0)
        self.db["old"].append(hash(joke))
        self.save_db()
        return joke

    def generate_new(self):
        raw_str = ""
        try:
            raw_str = Net.run(2000)
        except:
            raw_str = " \nthis is a test. jokebot will start producing jokes soon.\n "
        ret = raw_str.split("\n")
        if(len(ret) > 2):
            for new_joke in ret[1:-1]:
                h = hash(new_joke)
                if not h in self.db["old"]: 
                    self.db["new"] = ret[1:-1]
        else:
            self.db["new"] = ["Couldn't get any jokes from my stupid neural network, it did produce something but it's crap"]
        
