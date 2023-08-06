from imutils import face_utils
import imutils
import numpy as np
import collections
import dlib
import cv2
import skimage.draw
import scipy as sp
import scipy.spatial
from PIL import Image

class Face_cropper:
    def __init__(self, dlib_descriptor_filepath):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(dlib_descriptor_filepath)
    
    def crop_out_lips(self,filename):
        img = cv2.imread(filename)
        try:
            rect = self.detector(img)[0]
            sp = self.predictor(img, rect)
            landmarks = np.array([[p.x, p.y] for p in sp.parts()])
            outline = landmarks[[x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
            Y, X = skimage.draw.polygon(outline[:,1], outline[:,0])
            cropped_img = np.zeros(img.shape, dtype=np.uint8)
            cropped_img[Y, X] = img[Y, X]
            result_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(result_rgb)
        except IndexError:
            return False

    def crop_face_without_lips(self,filename):
        img = cv2.imread(filename)
        try:
            rect = self.detector(img)[0]
            sp = self.predictor(img, rect)
            landmarks = np.array([[p.x, p.y] for p in sp.parts()])
            outline = landmarks[[x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
            Y, X = skimage.draw.polygon(outline[:,1], outline[:,0])
            img[Y,X] = 0
            result_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(result_rgb)
        except IndexError:
            return False
    
    def isolate_mouth(self,filename, mouth_only = True,preImg = None):
        try:
            if preImg is None:
                img = cv2.imread(filename)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
                dets = self.detector(img, 1)
            else:
                pil_image = preImg.convert('RGB') 
                open_cv_image = np.array(pil_image)
                img = open_cv_image
                dets = self.detector(open_cv_image, 1)
            #print("Number of faces detected: {}".format(len(dets)))
            #result_rgb = False
            
            for k, d in enumerate(dets):
                #print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #   k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                shape = self.predictor(img, d)
                # The next lines of code just get the coordinates for the mouth
                # and crop the mouth from the image.This part can probably be optimised
                # by taking only the outer most points.
                xmouthpoints = [shape.part(x).x for x in range(48,67)]
                ymouthpoints = [shape.part(x).y for x in range(48,67)]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)

                pad = 10
                crop_image = img.copy()
                if mouth_only : 
                    crop_image = crop_image[miny-pad:maxy+pad,minx-pad:maxx+pad]
                else:
                    crop_image[0:miny-pad,0::] = 0 #haut
                    crop_image[maxy+pad::,0::] = 0 #bas
                    crop_image[0::,0:minx- pad] = 0 #gauche
                    crop_image[0::,maxx+pad::] = 0 #droite
                result_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            if len(dets) > 0:
                return Image.fromarray(result_rgb)
            return False
        except IndexError:
            return False
    
    def isolate_eye(self,filename, eye_only = True,preImg = None):
        try:
            if preImg is None:
                img = cv2.imread(filename)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
                dets = self.detector(img, 1)
            else:
                pil_image = preImg.convert('RGB') 
                open_cv_image = np.array(pil_image)
                img = open_cv_image
                dets = self.detector(open_cv_image, 1)
            #print("Number of faces detected: {}".format(len(dets)))
            #result_rgb = False
            
            for k, d in enumerate(dets):
                #print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #   k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                shape = self.predictor(img, d)
                # The next lines of code just get the coordinates for the mouth
                # and crop the mouth from the image.This part can probably be optimised
                # by taking only the outer most points.
                xmouthpoints = [shape.part(x).x for x in range(18,27)]
                ymouthpoints = [shape.part(x).y for x in range(37,48)]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)

                pad = 10
                crop_image = img.copy()
                if eye_only : 
                    crop_image = crop_image[miny-pad:maxy+pad,minx-pad:maxx+pad]
                else:
                    crop_image[0:miny-pad,0::] = 0 #haut
                    crop_image[maxy+pad::,0::] = 0 #bas
                    crop_image[0::,0:minx- pad] = 0 #gauche
                    crop_image[0::,maxx+pad::] = 0 #droite
                result_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            if len(dets) > 0:
                return Image.fromarray(result_rgb)
            return False
        except IndexError:
            return False

#Change version number and run :
# python3 setup.py sdist bdist_wheel