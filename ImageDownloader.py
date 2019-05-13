from google_images_download import google_images_download
import cv2
import os
import numpy as np
import time

class ImageDownloader:
    def __init__(self,image_download_directory):
        self.image_download_directory = image_download_directory
        self.save_size = 300
    
    def download_images(self,search_query,n_images):
        response = google_images_download.googleimagesdownload()
        absolute_image_paths = response.download({"keywords" : search_query,"limit" : int(n_images),"output_directory" : self.image_download_directory,"no_directory" : True})
        images = self.cleanup_images(absolute_image_paths[0])
        ret = []
        for i in range(len(images)):
            img_path = self.image_download_directory +"/" + search_query.replace(" ","_") + "_" + str(i) + ".png"
            cv2.imwrite(img_path,images[i])
            ret.append(img_path)
        if(len(ret) <= 0): #just to statisfy the criterion of having at least one image
            time.sleep(120)
            self.download_images(self,search_query,int(n_images + 5))
        return ret

    def cleanup_images(self,image_paths):
        parent_key = list(image_paths.keys())[0]
        ret = []
        for img_path in image_paths[parent_key]:
            img = cv2.imread(img_path)            
            if(img is None):
                os.remove(img_path)
                continue
            ratio = img.shape[0] / float(img.shape[1])
            img = cv2.resize(img,(self.save_size,int(self.save_size * ratio)),interpolation = cv2.INTER_CUBIC)
            img = self.subtract_background(img)
            ret.append(img.copy())
            os.remove(img_path)
        return ret

    def add_alpha_channel(self,img):
        b_channel, g_channel, r_channel = cv2.split(img)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) #creating a dummy alpha channel image.
        img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        return img_BGRA

    def subtract_background(self,img,thresh_val = 1):
        img_blurred = cv2.blur(img,(10,10))        
        img_filled = img_blurred.astype(np.float) / 255.0
        img_filled = img_filled * 250.0
        img_filled = img_filled.astype(np.uint8)
        h, w = img.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        thresh = (thresh_val,thresh_val,thresh_val,thresh_val)
        newVal = (255,255,255,255)
        cv2.floodFill(img_filled,mask = mask, seedPoint = (0, 0), newVal = newVal,loDiff = thresh,upDiff=thresh)
        cv2.floodFill(img_filled,mask = mask, seedPoint = (w-1, 0), newVal = newVal,loDiff = thresh,upDiff=thresh)
        cv2.floodFill(img_filled,mask = mask, seedPoint = (w-1, h-1), newVal = newVal,loDiff = thresh,upDiff=thresh)
        cv2.floodFill(img_filled,mask = mask, seedPoint = (0, h-1), newVal = newVal,loDiff = thresh,upDiff=thresh)
        cv2.floodFill(img_filled,mask = mask, seedPoint = (int(w/2), 0), newVal = newVal,loDiff = thresh,upDiff=thresh)
        cv2.floodFill(img_filled,mask = mask, seedPoint = (w-1, int(h/2)), newVal = newVal,loDiff = thresh,upDiff=thresh)
        cv2.floodFill(img_filled,mask = mask, seedPoint = (int(w/2), h-1), newVal = newVal,loDiff = thresh,upDiff=thresh)
        cv2.floodFill(img_filled,mask = mask, seedPoint = (0, int(h/2)), newVal = newVal,loDiff = thresh,upDiff=thresh)        
        img_filled = cv2.threshold(img_filled,252,255,cv2.THRESH_BINARY)[1]
        img_filled = 255-img_filled

        img_filled = img_filled.astype(float)
        img_filled = cv2.blur(img_filled,(5,5))
        ret = img.astype(float)
        ret = self.add_alpha_channel(ret)
        ret[:,:,3] = img_filled[:,:,0]
        return ret

