from ClipartDatabase import *
from PIL import Image, ImageDraw, ImageFont
import random
import time

class JokeDrawer:
    def __init__(self):    
        self.cliparts = ClipartDatabase("clipart")
        self.font = ImageFont.truetype('font.ttf',60)
        self.tiny_image = Image.new('RGB',(1,1),(255,255,255))
        self.padding = 20
    
    def draw_joke(self,joke_text,filename):
        #first make the text formatting
        #to acquire the image size
        keywords = self.get_keywords(joke_text,random.randint(4,8))#get 4 - 8 keywords
        joke_text = self.format_joke(joke_text,max_line_len = 30)
        image_size = self.get_image_size(joke_text)
        bg_color = self.get_bg_color()
        joke_image = Image.new('RGBA',(image_size,image_size),bg_color)

        self.draw_cliparts(joke_image,keywords)
        self.draw_text(joke_image,joke_text,bg_color)    
        
        joke_image.save(filename)
    
    def get_bg_color(self):
        return (random.randint(127,255),random.randint(127,255),random.randint(127,255),255)
    
    def draw_cliparts(self,image,keywords):
        clipart_positions = self.get_clipart_positions(image,len(keywords))
        for i in range(len(keywords)):
            keywd = keywords[i]
            filename = self.cliparts.get_clipart(keywd)
            if(filename is None):
                continue
            clipart = Image.open(filename, 'r')
            cl_w, cl_h = clipart.size
            position = clipart_positions[i]
            image.paste(clipart, position,clipart)
    
    def draw_text(self,image,text,bg_color):
        drawer = ImageDraw.Draw(image)  
        txt_size = self.text_size(text)
        y_offset = (max(txt_size[0],txt_size[1]) - txt_size[1]) / 2
        drawer.text((self.padding+3,self.padding+3+y_offset), text, font=self.font, fill=(255,255,255))  
        drawer.text((self.padding+3,self.padding-3+y_offset), text, font=self.font, fill=(255,255,255))
        drawer.text((self.padding-3,self.padding-3+y_offset), text, font=self.font, fill=(255,255,255))
        drawer.text((self.padding-3,self.padding+3+y_offset), text, font=self.font, fill=(255,255,255))  
        drawer.text((self.padding,self.padding+y_offset), text, font=self.font, fill=(0,0,0))    
    
    def get_clipart_positions(self,image,n_pos):  
        ret = []
        bg_w, bg_h = image.size
        for i in range(n_pos):
            new_pos = (0,0)
            good_pos = False
            start_time = time.time()
            while not good_pos:
                new_pos = (random.randint(0,bg_w-300),random.randint(0,bg_h-300))
                good_pos = True                
                for pos in ret:
                    delta = [pos[0] - new_pos[0],pos[1] - new_pos[1]]
                    dist = delta[0] * delta[0] + delta[1] * delta[1]
                    if(dist < 300*300):
                        good_pos = False
                        break
                if(time.time() - start_time) > 2: #if you failed to find a good pos for 2 seconds, just scrap it.
                    good_pos = True
            ret.append(new_pos)
        return ret
    
    def get_image_size(self,text):
        size = self.text_size(text)
        return max(size[0],size[1]) + 2*self.padding
    
    def text_size(self,txt):
        d = ImageDraw.Draw(self.tiny_image)
        ret = d.textsize(txt,font=self.font)
        return ret

    def get_keywords(self,text,n_keywords):
        ret = []
        word_arr = text.split(" ")
        big_word_arr = []
        for word in word_arr:
            if(len(word) >= 3):
                big_word_arr.append(word)
        #i need to introduce a chance 
        good_keywds = ["funny","haha","laughing","joke","robot"]
        ret.append(random.choice(good_keywds))
        n_keywords -= 1
        for i in range(n_keywords):
            keywd = random.choice(big_word_arr)
            keywd = keywd.lower()
            keywd = self.remove_all_but(keywd,"abcdefghijklmnopqrstuvwxyz")
            ret.append(keywd)
        return ret

    def remove_all_but(self,text,allowed):
        ret = ""
        for c in text:
            if(c in allowed):
                ret += c
        return ret

    def format_joke(self,text,max_line_len):   
        ret = ""
        text_arr = text.split(" ")
        current_len = 0
        for word in text_arr:
            if(current_len > max_line_len):
                ret += "\n"
                current_len = 0
            ret += word + " "    
            if(len(word) > 1):
                if(word[-1] in ".?!\""):
                    ret += "\n"
                    current_len = 0         
            current_len += len(word)
        return ret
