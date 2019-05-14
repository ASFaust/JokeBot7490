from JokeGenerator import *
from JokeDrawer import *
from FacebookPage import *
import time

class JokeBot7490:
    def __init__(self):
        self.generator = JokeGenerator("joke_database.json")
        self.drawer = JokeDrawer()        
        self.fb = FacebookPage()

    def main_loop(self):        
        while(True):
            start_time = time.time()
            joke_text = self.generator.get_joke()
            self.drawer.draw_joke(joke_text,"out.png")
            self.fb.post_image("out.png","This is a test. jokebot is coming back soon.")
            
            delta_time = time.time() - start_time            
            time.sleep(max(10*60,30*60 - delta_time))

'''

jg = JokeGenerator("joke_database.json")

for i in range(0,20):
    print(jg.get_joke())



from JokeDrawer import *

jd = JokeDrawer()

jd.draw_joke("Why did the feminist go to the store? Because he was in denial","out_1.png")
jd.draw_joke("Why did the walrus get off the swings? Because she wasn't a good credit for the first time.","out_2.png")
jd.draw_joke("I was fat for hundreds of balls... And I gave him a good explorer.","out_3.png")
jd.draw_joke("No pun in ten didn't hold my new plastic one... I said \"I have a hairdress and I'm not really crying tonight.\" And the potential salesman's new day and I started this one. I bet you have cats. Me: No, he has a real taste funny joke.","out_4.png")
jd.draw_joke("What do you call a group of sad? A white person.","out_5.png")

'''

