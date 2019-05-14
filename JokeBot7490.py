from JokeGenerator import *
from JokeDrawer import *
from FacebookPage import *
import time
import Log

class JokeBot7490:
    def __init__(self):
        self.generator = JokeGenerator("joke_database.json")
        self.drawer = JokeDrawer()        
        self.fb = FacebookPage()
        self.log = Log.Logger("logs/log.log")

    def main_loop(self):        
        while(True):
            start_time = time.time()
            self.log.put("getting joke")
            joke_text = self.generator.get_joke()
            self.log.put("drawing joke")
            self.drawer.draw_joke(joke_text,"out.png")
            self.log.put("posting joke")
            self.fb.post_image("out.png","HERE IS YOUR JOKE") 
            delta_time = time.time() - start_time
            self.log.put("took " + str(delta_time) + " seconds to generate post")   
            time.sleep(max(10*60,30*60 - delta_time))

