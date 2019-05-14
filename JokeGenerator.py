import os
import random
import json
import Net
import hashlib
import Log

class JokeGenerator:
    def __init__(self,joke_db):
        self.db_filename = joke_db
        self.db = {}
        self.replacement_dict = {}
        self.net_success = False
        self.log = Log.Logger("logs/log.log")
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
            self.log.put("need to generate new jokes")
            self.generate_new() 
            self.log.put("finished generating new jokes")
        joke = self.db["new"].pop(0)
        if(self.net_success):
            self.db["old"].append(hash(joke))
        self.save_db()
        self.log.put("returning joke: " + joke)
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
        raw_str = " \nnothing\n "
        self.net_success = True
        try:
            self.log.put("running net")
            start_time = time.time()
            raw_str = Net.run(1000) #runs the net for 2000 characters
            delta_time = time.time() - start_time
            self.log.put("finished running net. took " + str(delta_time) + " seconds, that's " + str(1000.0 / delta_time) + " seconds per character")
            self.log.put(type(raw_str))
            self.log.put(str(raw_str))
            self.net_success = True
        except:        
            raw_str = " \nif this message shows up, something went wrong\n "
            self.net_success = False
            self.log.put("couldn't run net")
        new_joke_arr = []
        new_joke_arr = str(raw_str).split("\n")
        if(len(new_joke_arr) > 2):
            for new_joke in new_joke_arr[1:-1]:
                new_joke_pc = self.make_PC(new_joke)
                h = hash(new_joke_pc)
                if not h in self.db["old"]: 
                    self.db["new"].append(new_joke_pc)
        else:
            self.db["new"] = ["Couldn't get any jokes from my stupid neural network, it did produce something but it's crap"]   
            self.net_success = False
        self.log.put("generated " + str(len(self.db["new"])) + " new jokes")


        
