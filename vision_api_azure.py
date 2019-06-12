#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs
import subprocess

import cv2
import requests
import json



# azure 画像認識、OCR認識
import vision_api_azure_key as azure_key



class VisionAPI:

    def __init__(self, ):
        self.timeOut = 10
        self.cv_url  = None
        self.cv_key  = None
        self.ocr_url = None
        self.ocr_key = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, url, key, ):
        # azure 画像認識
        if (api == 'cv'):
            self.cv_url = url
            self.cv_key = key
            if (not self.cv_key is None):
                return True

        # azure OCR認識
        if (api == 'ocr'):
            self.ocr_url = url
            self.ocr_key = key
            if (not self.ocr_key is None):
                return True

        return False



    def convert(self, inpImage, outImage, bw=True, maxWidth=640, maxHeight=480, ):
        try:
            if (os.path.exists(outImage)):
                os.remove(outImage)

            image_img = cv2.imread(inpImage, cv2.IMREAD_UNCHANGED)
            if len(image_img.shape) == 3:
                image_height, image_width, image_channels = image_img.shape[:3]
            else:
                image_height, image_width = image_img.shape[:2]
                image_channels = 1

            proc_img    = image_img.copy()
            proc_width  = image_width
            proc_height = image_height
            if (bw == True):
                if (image_channels != 1):
                    proc_img = cv2.cvtColor(image_img, cv2.COLOR_BGR2GRAY)

                #proc_img = cv2.equalizeHist(proc_img)
                #proc_img = cv2.blur(proc_img, (3,3), 0)
                #_, proc_img = cv2.threshold(proc_img, 140, 255, cv2.THRESH_BINARY)

            if (maxWidth != 0):
                if (proc_width > maxWidth):
                    proc_height = int(proc_height * (maxWidth / proc_width))
                    proc_width  = maxWidth
                    proc_img = cv2.resize(proc_img, (proc_width, proc_height))

            if (maxHeight != 0):
                if (proc_height > maxHeight):
                    proc_width  = int(proc_width * (maxHeight / proc_height))
                    proc_height = maxHeight
                    proc_img = cv2.resize(proc_img, (proc_width, proc_height))

            if (maxWidth != 0) and (maxWidth != 0):
                if (proc_width > maxWidth) or (proc_height > maxHeight):
                    proc_width  = maxWidth
                    proc_height = maxHeight
                    proc_img = cv2.resize(proc_img, (proc_width, proc_height))

            cv2.imwrite(outImage, proc_img)
            return True

        except:
            pass

        return False



    def cv(self, inpImage, inpLang='ja', ):
        res_text = None
        res_api  = ''

        if (self.cv_key == None):
            print('AZURE: Not Authenticate Error !')

        else:
            lang = inpLang

            if (True):
                try:
                    rb = open(inpImage, 'rb')
                    photo = rb.read()
                    rb.close
                    rb = None

                    url  = self.cv_url
                    headers = {
                        'Content-Type': 'application/octet-stream',
                        'Ocp-Apim-Subscription-Key': self.cv_key
                        }
                    params = {
                        'visualFeatures': 'Categories,Description',
                        'language': lang,
                        }
                    res = requests.post(url, headers=headers, params=params, data=photo, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        res_json = json.loads(res.text)
                        #print(res_json)
                        categories  = ''
                        captions    = ''
                        description = ''
                        try:
                            for names in res_json.get('categories'):
                                nm = str(names.get('name')).replace('_',' ')
                                categories += nm.strip() + ','
                        except:
                            pass

                        try:
                            for texts in res_json.get('description').get('captions'):
                                cp = str(texts.get('text'))
                                captions = cp.strip() + ','
                        except:
                            pass

                        try:
                            for tag in res_json.get('description').get('tags'):
                                description += str(tag).strip() + ','
                        except:
                            pass

                        res_text = {}
                        res_text['categories']  = categories
                        res_text['captions']    = captions
                        res_text['description'] = description
                except:
                    pass

            return res_text, 'azure'

        return None, ''

    def ocr(self, inpImage, inpLang='ja', ):
        res_text = None
        res_api  = ''

        if (self.ocr_key == None):
            print('AZURE: Not Authenticate Error !')

        else:
            lang = inpLang

            if (True):
                try:
                    rb = open(inpImage, 'rb')
                    photo = rb.read()
                    rb.close
                    rb = None

                    url  = self.ocr_url
                    headers = {
                        'Content-Type': 'application/octet-stream',
                        'Ocp-Apim-Subscription-Key': self.ocr_key
                        }
                    params = {
                        'language': lang,
                        'detectOrientation': 'true',
                        }
                    res = requests.post(url, headers=headers, params=params, data=photo, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        res_json = json.loads(res.text)
                        #print(res_json)

                        res_text = []
                        try:
                            for region in res_json.get('regions'):
                                for line in region.get('lines'):
                                    s = ''
                                    for word in line.get('words'):
                                        s += word.get('text')
                                    #print( s )
                                    res_text.append(s)
                        except:
                            res_text = None
                except:
                    pass

            return res_text, 'azure'

        return None, ''



if __name__ == '__main__':

        #azureAPI = azure_api.VisionAPI()
        azureAPI = VisionAPI()

        res1 = azureAPI.authenticate('cv' ,
                    azure_key.getkey('cv' ,'url'),
                    azure_key.getkey('cv' ,'key'), )
        res2 = azureAPI.authenticate('ocr',
                    azure_key.getkey('ocr','url'),
                    azure_key.getkey('ocr','key'), )
        print('authenticate:', res1, res2)
        if (res1 == True) and (res2 == True):

            file = 'vision__cv_photo.jpg'
            temp = 'temp_cv_photo.jpg'

            res = azureAPI.convert(inpImage=file, outImage=temp, bw=False, )
            if (res == True):
                res, api = azureAPI.cv(inpImage=temp, inpLang='ja', )
                if (not res is None):
                    print('cv')
                    print('categories:', res['categories'], '(' + api + ')' )
                    print('captions:', res['captions']   , '(' + api + ')' )
                    print('description:', res['description'], '(' + api + ')' )

            res = azureAPI.convert(inpImage=file, outImage=temp, bw=True, )
            if (res == True):
                res, api = azureAPI.ocr(inpImage=temp, inpLang='ja', )
                if (not res is None):
                    print('ocr1')
                    for text in res:
                        print('ocr:', text, '(' + api + ')' )

            file = 'vision__ocr_photo.jpg'
            temp = 'temp_ocr_photo.jpg'

            res = azureAPI.convert(inpImage=file, outImage=temp, bw=True, )
            if (res == True):
                res, api = azureAPI.ocr(inpImage=temp, inpLang='ja', )
                if (not res is None):
                    print('ocr2')
                    for text in res:
                        print('ocr:', text, '(' + api + ')' )



