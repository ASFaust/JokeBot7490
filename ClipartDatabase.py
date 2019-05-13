from ImageDownloader import *
import os
import random

class ClipartDatabase:
    def __init__(self,base_folder):
        if not os.path.isdir(base_folder):
            os.mkdir(base_folder)
        if not os.path.isdir("download"):
            os.mkdir("download")
        self.base_folder = base_folder
        self.image_downloader = ImageDownloader("download")
    
    def get_clipart(self,keyword):
        img_dir = self.base_folder + "/" + keyword
        if(not os.path.isdir(img_dir)):
            os.mkdir(img_dir)
            dl_images = self.image_downloader.download_images(keyword + " clipart",25)
            for image_path in dl_images:
                os.rename(image_path,img_dir + "/" + image_path[image_path.rfind("/") + 1:])
        all_clips = os.listdir(img_dir)
        if(len(all_clips) <= 0):
            return None
        return self.base_folder + "/" + keyword + "/" + random.choice(all_clips)

