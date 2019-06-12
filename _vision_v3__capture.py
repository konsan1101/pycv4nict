#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import queue
import threading
import subprocess
import datetime
import time
import codecs
import glob

import platform
qOS = platform.system().lower() #windows,darwin,linux

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

print(os.path.dirname(__file__))
print(os.path.basename(__file__))
print(sys.version_info)



qApiCV     = 'google'
qApiOCR    = qApiCV
qApiTrn    = qApiCV
qLangCV    = 'ja'
qLangOCR   = qLangCV
qLangTrn   = 'en'

qPathDetect= 'temp/v3_1detect/'
qPathPhoto = 'temp/v3_2photo/'
qPathCv    = 'temp/v3_3cv_txt/'
qPathRec   = 'temp/v3_8recorder/'
qPathWork  = 'temp/v3_9work/'

qCtrlResultCV  = 'temp/temp_resultCV.txt'
qCtrlResultOCR = 'temp/temp_resultOCR.txt'
qCtrlResultTrn = 'temp/temp_resultTrn.txt'
qCtrlVision    = 'temp/temp_vision.txt'
qCtrlRecognize = 'temp/temp_recognize.txt'
qCtrlTranslate = 'temp/temp_translate.txt'

qFONT_default = {'file':'_vision_font_ipaexg.ttf','offset':10}
qFONT_zh = {'file':'C:/Windows/Fonts/msyh.ttc', 'offset':5}
qFONT_ko = {'file':'C:/Windows/Fonts/batang.ttc', 'offset':10}

qPathTTS   = 'temp/a3_5tts_txt/'
qPathWorkA = 'temp/a3_9work/'
qBusyCtrl  = qPathWorkA + 'busy_speechctl.txt'
qBusyInput = qPathWorkA + 'busy_voice2wav.txt'
qBusySTT   = qPathWorkA + 'busy_sttcore.txt'
qBusyTTS   = qPathWorkA + 'busy_ttscore.txt'
qBusyPlay  = qPathWorkA + 'busy_playvoice.txt'



def qBusyCheck(file, sec):
    chktime = time.time()
    while (os.path.exists(file)) and ((time.time() - chktime) < sec):
        time.sleep(0.10)
    if (os.path.exists(file)):
        return 'busy'
    else:
        return 'none'

def speech_wait(idolsec=2, maxwait=15, ):
    global qBusyCtrl
    global qBusyInput
    global qBusySTT
    global qBusyTTS
    global qBusyPlay

    busy_flag = True
    chktime1 = time.time()
    while (busy_flag == True) and ((time.time() - chktime1) < maxwait):
        busy_flag = False
        chktime2 = time.time()
        while ((time.time() - chktime2) < idolsec):
            if (qBusyCheck(qBusySTT , 0) == 'busy') \
            or (qBusyCheck(qBusyTTS , 0) == 'busy') \
            or (qBusyCheck(qBusyPlay, 0) == 'busy'):
                busy_flag = True
                time.sleep(0.10)
                break

def tts_speech(runMode, id, speechText, idolsec=2, maxwait=15, ):
    global qPathTTS

    speech_wait(idolsec,maxwait)

    print(speechText)
    if (speechText != ''):
        now=datetime.datetime.now()
        stamp=now.strftime('%Y%m%d-%H%M%S')
        wrkFile = qPathTTS + stamp + '.' + id + '.txt'

        try:
            w = codecs.open(wrkFile, 'w', 'utf-8')
            w.write(speechText)
            w.close()
            w = None
        except:
            w = None



def qMakeDirs(pPath, pRemove=False):
        #try:
        if (len(pPath) > 0):
            path=pPath.replace('\\', '/')
            if (path[-1:] != '/'):
                path += '/'
            if (not os.path.isdir(path[:-1])):
                os.makedirs(path[:-1])
            else:
                if (pRemove == True):
                    files = glob.glob(path + '*')
                    for f in files:
                        try:
                            os.remove(f)
                        except:
                            pass
        #except:
        #pass

qLogNow=datetime.datetime.now()
qLogFlie = 'temp/_log/' + qLogNow.strftime('%Y%m%d-%H%M%S') + '_' + os.path.basename(__file__) + '.log'
def qLogOutput(pLogText='', pDisplay=True, pOutfile=True):
        #try:
        if (pDisplay == True):
            print(str(pLogText))
        if (pOutfile == True):
            w = codecs.open(qLogFlie, 'a', 'utf-8')
            w.write(str(pLogText) + '\n')
            w.close()
            w = None
        #except:
        #pass

qMakeDirs('temp/_log/', False)
qLogOutput(qLogFlie, True, True)

def qGuide(tempFile=None, sync=True):
    if (tempFile == '_up'):
        tempFile = '_sound_up.mp3'
    if (tempFile == '_ready'):
        tempFile = '_sound_ready.mp3'
    if (tempFile == '_accept'):
        tempFile = '_sound_accept.mp3'
    if (tempFile == '_ok'):
        tempFile = '_sound_ok.mp3'
    if (tempFile == '_ng'):
        tempFile = '_sound_ng.mp3'
    if (tempFile == '_down'):
        tempFile = '_sound_down.mp3'
    if (tempFile == '_shutter'):
        tempFile = '_sound_shutter.mp3'

    if (os.path.exists(tempFile)):

        sox=subprocess.Popen(['sox', '-q', tempFile, '-d', ], \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        if (sync == True):
            sox.wait()
            sox.terminate()
            sox = None



def qGetResolution(reso='full'):
    global qOS

    if   (reso=='full'):
        if (qOS != 'darwin'):
            return 1920,1080
        else:
            return 2560,1600
    elif (reso=='half'):
        if (qOS != 'darwin'):
            return 960,540
        else:
            return 1280,800
    elif (reso=='vga'):
            return 640,480
    elif (reso=='dvd'):
            return 720,480
    elif (reso=='1280x720'):
            return 1280,720
    return 640,480



class qFPS(object):
    def __init__(self):
        self.start = cv2.getTickCount()
        self.count = 0
        self.FPS   = 0
    def get(self):
        self.count += 1
        if (self.count >= 30):
            nowTick  = cv2.getTickCount()
            diffSec  = (nowTick - self.start) / cv2.getTickFrequency()
            self.FPS = 1 / (diffSec / self.count)
            self.start = cv2.getTickCount()
            self.count = 0
        return self.FPS



inp1_Height= 0
inp1_Width = 0
inp1_Image = None
inp1_FPS   = 0
inp1_Zoom  = '1.0'

inp1_start = 0
inp1_beat  = 0
inp1_busy  = False
inp1_last  = 0
inp1_seq   = 0
def proc_inp1(cn_r, cn_s, ):
    global inp1_Height
    global inp1_Width
    global inp1_Image
    global inp1_FPS
    global inp1_Zoom

    global inp1_start
    global inp1_beat
    global inp1_busy
    global inp1_last
    global inp1_seq

    qLogOutput('video_inp1:init')

    runMode    = cn_r.get()
    cam1Dev    = cn_r.get()
    cam1Rotate = int(cn_r.get())
    cam1Mode   = cn_r.get()
    cam1Zoom   = cn_r.get()
    cam1Width,cam1Height = qGetResolution(cam1Mode)
    cam1Fps    = 30
    dspMode    = cn_r.get()
    dspWidth,dspHeight = qGetResolution(dspMode)
    cn_r.task_done()

    qLogOutput('video_inp1:runMode   =' + str(runMode   ))
    qLogOutput('video_inp1:cam1Dev   =' + str(cam1Dev   ))
    qLogOutput('video_inp1:cam1Rotate=' + str(cam1Rotate))
    qLogOutput('video_inp1:cam1Mode  =' + str(cam1Mode  ))
    qLogOutput('video_inp1:cam1Zoom  =' + str(cam1Zoom  ))
    qLogOutput('video_inp1:cam1Width =' + str(cam1Width ))
    qLogOutput('video_inp1:cam1Height=' + str(cam1Height))
    qLogOutput('video_inp1:cam1Fps   =' + str(cam1Fps   ))
    qLogOutput('video_inp1:dspMode   =' + str(dspMode   ))
    qLogOutput('video_inp1:dspWidth  =' + str(dspWidth  ))
    qLogOutput('video_inp1:dspHeight =' + str(dspHeight ))

    capture = None
    if (cam1Dev.isdigit()):
        capture = cv2.VideoCapture(int(cam1Dev))
        try:
            capture.set(3, int(cam1Width ))
            capture.set(4, int(cam1Height))
            capture.set(5, int(cam1Fps   ))
        except:
            pass
    else:
        capture = cv2.VideoCapture(cam1Dev)

    qLogOutput('video_inp1:start')
    inp1_start = time.time()

    fps_class = qFPS()
    while (True):
        inp1_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('video_inp1:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qLogOutput('video_inp1: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                cn_s.put(['PASS', ''])

            elif (mode_get == 'ZOOM'):
                cam1Zoom = data_get
                cn_s.put(['OK', ''])

            else:
                inp1_busy = True
                ret, frame = capture.read()

                if (ret == False):
                    qLogOutput('video_inp1:capture error')
                    time.sleep(5.00)
                    cn_s.put(['END', ''])
                    time.sleep(5.00)
                    break

                else:
                    inp1_FPS = fps_class.get()

                    # frame_img
                    inp1_Height, inp1_Width = frame.shape[:2]
                    inp1_Image = frame.copy()

                    # image_img
                    if abs(int(cam1Rotate)) == 90:
                        inp1_Width2 = int((inp1_Width - inp1_Height)/2)
                        rect_img    = cv2.resize(inp1_Image[0:inp1_Height, inp1_Width2:inp1_Height], (960,960))
                        rect_mat    = cv2.getRotationMatrix2D((960, 960), int(cam1Rotate), 1.0)
                        rect_r      = cv2.warpAffine(rect_img, rect_mat, (960, 960), flags=cv2.INTER_LINEAR)
                        display_img = cv2.resize(rect_r, (dspWidth, dspHeight))
                    elif abs(int(cam1Rotate)) == 180:
                        display_img = cv2.resize(inp1_Image, (dspWidth, dspHeight))
                        display_img = cv2.flip(display_img, 0) # 180 Rotation
                    else:
                        display_img = cv2.resize(inp1_Image, (dspWidth, dspHeight))

                    inp1_Zoom = cam1Zoom
                    if (inp1_Zoom != '1.0'):
                        zm = float(inp1_Zoom)
                        x1 = int((dspWidth-(dspWidth/zm))/2)
                        x2 = dspWidth - x1
                        y1 = int((dspHeight-(dspHeight/zm))/2)
                        y2 = dspHeight - y1
                        zm_img = display_img[y1:y2, x1:x2]
                        display_img = cv2.resize(zm_img, (dspWidth, dspHeight))

                    cn_s.put(['IMAGE', display_img.copy()])

        inp1_busy = False
        if (cn_r.qsize() == 0):
            time.sleep(0.05)
        else:
            time.sleep(0.01)

    qLogOutput('video_inp1:terminate')

    capture.release()

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('video_inp1:end')



inp2_Height= 0
inp2_Width = 0
inp2_Image = None
inp2_FPS   = 0
inp2_Zoom  = '1.0'

inp2_start = 0
inp2_beat  = 0
inp2_busy  = False
inp2_last  = 0
inp2_seq   = 0
def proc_inp2(cn_r, cn_s, ):
    global inp2_Height
    global inp2_Width
    global inp2_Image
    global inp2_FPS
    global inp2_Zoom

    global inp2_start
    global inp2_beat
    global inp2_busy
    global inp2_last
    global inp2_seq

    qLogOutput('video_inp2:init')

    runMode    = cn_r.get()
    cam2Dev    = cn_r.get()
    cam2Rotate = int(cn_r.get())
    cam2Mode   = cn_r.get()
    cam2Zoom   = cn_r.get()
    cam2Width,cam2Height = qGetResolution(cam2Mode)
    cam2Fps   = 30
    cn_r.task_done()

    qLogOutput('video_inp2:runMode   =' + str(runMode   ))
    qLogOutput('video_inp2:cam2Dev   =' + str(cam2Dev   ))
    qLogOutput('video_inp2:cam2Rotate=' + str(cam2Rotate))
    qLogOutput('video_inp2:cam2Mode  =' + str(cam2Mode  ))
    qLogOutput('video_inp2:cam2Zoom  =' + str(cam2Zoom  ))
    qLogOutput('video_inp2:cam2Width =' + str(cam2Width ))
    qLogOutput('video_inp2:cam2Height=' + str(cam2Height))
    qLogOutput('video_inp2:cam2Fps   =' + str(cam2Fps   ))

    capture = None
    if (cam2Dev.isdigit()):
        capture = cv2.VideoCapture(int(cam2Dev))
        try:
            capture.set(3, int(cam2Width ))
            capture.set(4, int(cam2Height))
            capture.set(5, int(cam2Fps   ))
        except:
            pass
    else:
        capture = cv2.VideoCapture(cam2Dev)

    qLogOutput('video_inp2:start')
    inp2_start = time.time()

    fps_class = qFPS()
    while (True):
        inp2_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('video_inp2:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qLogOutput('video_inp2: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                cn_s.put(['PASS', ''])

            elif (mode_get == 'ZOOM'):
                cam2Zoom = data_get
                cn_s.put(['OK', ''])

            else:
                inp2_busy = True
                ret, frame = capture.read()

                if (ret == False):
                    qLogOutput('video_inp2:capture error')
                    time.sleep(5.00)
                    cn_s.put(['END', ''])
                    time.sleep(5.00)
                    break

                else:
                    inp2_FPS = fps_class.get()

                    # frame_img
                    inp2_Height, inp2_Width = frame.shape[:2]
                    inp2_Image = frame.copy()

                    # image_img
                    if abs(int(cam2Rotate)) == 90:
                        inp2_Width2 = int((inp2_Width - inp2_Height)/2)
                        rect_img    = cv2.resize(inp2_Image[0:inp2_Height, inp2_Width2:inp2_Height], (960,960))
                        rect_mat    = cv2.getRotationMatrix2D((960, 960), int(cam2Rotate), 1.0)
                        rect_r      = cv2.warpAffine(rect_img, rect_mat, (960, 960), flags=cv2.INTER_LINEAR)
                        display_img = cv2.resize(rect_r, (cam2Width, cam2Height))
                    elif abs(int(cam2Rotate)) == 180:
                        display_img = cv2.resize(inp2_Image, (cam2Width, cam2Height))
                        display_img = cv2.flip(display_img, 0) # 180 Rotation
                    else:
                        display_img = cv2.resize(inp2_Image, (cam2Width, cam2Height))

                    inp2_Zoom = cam2Zoom
                    if (inp2_Zoom != '1.0'):
                        zm = float(inp2_Zoom)
                        x1 = int((cam2Width-(cam2Width/zm))/2)
                        x2 = cam2Width - x1
                        y1 = int((cam2Height-(cam2Height/zm))/2)
                        y2 = cam2Height - y1
                        zm_img = display_img[y1:y2, x1:x2]
                        display_img = cv2.resize(zm_img, (cam2Width, cam2Height))

                    cn_s.put(['IMAGE', display_img.copy()])

        inp2_busy = False
        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.05)

    qLogOutput('video_inp2:terminate')

    capture.release()

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('video_inp2:end')



compute_start = 0
compute_beat  = 0
compute_busy  = False
compute_last  = 0
compute_seq   = 0
def proc_compute(cn_r, cn_s, ):
    global qPathDetect
    global qPathPhoto
    global qPathRec

    global compute_start
    global compute_beat
    global compute_busy
    global compute_last
    global compute_seq

    proc_width,proc_height = qGetResolution('full')
    proc_width  = int(proc_width  / 4)
    proc_height = int(proc_height / 4)

    qLogOutput('v_compute_:init')

    runMode   = cn_r.get()
    cam1Dev   = cn_r.get()
    casName1  = cn_r.get()
    casName2  = cn_r.get()
    cn_r.task_done()

    qLogOutput('v_compute_:runMode   =' + str(runMode ))
    qLogOutput('v_compute_:cam1Dev   =' + str(cam1Dev ))
    if (casName1 != 'none'):
        cas_nm1 = casName1[:-4]
        cas_nm1 = cas_nm1.replace('_vision_opencv_', '')
        qLogOutput('v_compute_:casName1  =' + str(casName1  ))
        cascade1 = cv2.CascadeClassifier(casName1)
        haar_scale1    = 1.1
        min_neighbors1 = 10
        min_size1      = ( 15, 15)
        if (casName1 == '_vision_opencv_cars.xml'):
            haar_scale1    = 1.1
            min_neighbors1 = 3
            min_size1      = ( 15, 15)
    if (casName2 != 'none'):
        cas_nm2 = casName2[:-4]
        cas_nm2 = cas_nm2.replace('_vision_opencv_', '')
        qLogOutput('v_compute_:casName2  =' + str(casName2  ))
        cascade2 = cv2.CascadeClassifier(casName2)
        haar_scale2    = 1.1
        min_neighbors2 = 15
        min_size2      = ( 20, 20)
        if (casName2 == '_vision_opencv_cars.xml'):
            haar_scale2    = 1.1
            min_neighbors2 = 5
            min_size2      = ( 20, 20)

    qLogOutput('v_compute_:start')
    compute_start = time.time()

    while (True):
        compute_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('v_compute_:None=break')
                break

            #if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
            if (cn_r.qsize() > 3) or (cn_s.qsize() > 3):
                qLogOutput('v_compute_: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                cn_s.put(['PASS', ''])

            else:
                compute_busy = True
                res_put = False

                if (mode_get == 'INPUT'):
                    image_img   = data_get.copy()
                    image_height, image_width = image_img.shape[:2]
                    proc_img    = image_img.copy()
                    proc_height = int(proc_width * image_height / image_width)

                    gray  = cv2.resize(image_img, (proc_width, proc_height))
                    gray1 = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
                    gray2 = cv2.equalizeHist(gray1)

                    hit_count  = 0
                    hit_count1 = 0
                    hit_count2 = 0
                    hit_img1   = None
                    hit_img2   = None

                    now=datetime.datetime.now()
                    stamp=now.strftime('%Y%m%d.%H%M%S')

                    filename=qPathRec + stamp + '.' + cas_nm1 + '.jpg'
                    #if (casName1 != 'none') and (not os.path.exists(filename)):
                    if (casName1 != 'none'):
                        rects1 = cascade1.detectMultiScale(gray2, scaleFactor=haar_scale1, minNeighbors=min_neighbors1, minSize=min_size1)
                        if (not rects1 is None):
                            for (hit_x, hit_y, hit_w, hit_h) in rects1:
                                hit_count  += 1
                                hit_count1 += 1
                                x  = int(hit_x * image_width  / proc_width )
                                y  = int(hit_y * image_height / proc_height)
                                w  = int(hit_w * image_width  / proc_width )
                                h  = int(hit_h * image_height / proc_height)
                                if (cas_nm1 == 'face'):
                                    if (x > 10):
                                        x -= 10
                                        w += 20
                                    if (y > 10):
                                        y -= 10
                                        h += 20
                                if (x < 0):
                                    x = 0
                                if (y < 0):
                                    y = 0
                                if ((x + w) > image_width):
                                     w = image_width - x
                                if ((y + h) > image_height):
                                     h = image_height - y
                                cv2.rectangle(proc_img, (x,y), (x+w,y+h), (0,0,255), 2)

                                if (hit_count1 == 1):
                                    hit_img1 = cv2.resize(image_img[y:y+h, x:x+w],(h,w))

                                    filename1=filename
                                    filename2=filename.replace(qPathRec, qPathDetect)
                                    if (not os.path.exists(filename1)) and (not os.path.exists(filename2)):
                                        try:
                                                cv2.imwrite(filename1, hit_img1)
                                                cv2.imwrite(filename2, hit_img1)
                                        except:
                                                pass
                                        qLogOutput(u'v_compute_: → ' + filename2)
                                        filename1=qPathPhoto + stamp + '.detect.jpg'
                                        filename2=qPathRec   + stamp + '.detect.jpg'
                                        if (not os.path.exists(filename1)) and (not os.path.exists(filename2)):
                                            try:
                                                cv2.imwrite(filename1, image_img)
                                                cv2.imwrite(filename2, image_img)
                                            except:
                                                pass

                    filename=qPathRec + stamp + '.' + cas_nm2 + '.jpg'
                    #if (casName2 != 'none') and (not os.path.exists(filename)):
                    if (casName2 != 'none'):
                        rects2 = cascade2.detectMultiScale(gray2, scaleFactor=haar_scale2, minNeighbors=min_neighbors2, minSize=min_size2)
                        if (not rects2 is None):
                            for (hit_x, hit_y, hit_w, hit_h) in rects2:
                                hit_count  += 1
                                hit_count2 += 1
                                x  = int(hit_x * image_width  / proc_width )
                                y  = int(hit_y * image_height / proc_height)
                                w  = int(hit_w * image_width  / proc_width )
                                h  = int(hit_h * image_height / proc_height)
                                if (x < 0):
                                    x = 0
                                if (y < 0):
                                    y = 0
                                if ((x + w) > image_width):
                                     w = image_width - x
                                if ((y + h) > image_height):
                                     h = image_height - y
                                cv2.rectangle(proc_img, (x,y), (x+w,y+h), (0,255,0), 2)

                                if (hit_count2 == 1):
                                    hit_img2 = cv2.resize(image_img[y:y+h, x:x+w],(h,w))

                                    filename1=filename
                                    filename2=filename.replace(qPathRec, qPathDetect)
                                    if (not os.path.exists(filename1)) and (not os.path.exists(filename2)):
                                        try:
                                                cv2.imwrite(filename1, hit_img2)
                                                cv2.imwrite(filename2, hit_img2)
                                        except:
                                                pass
                                        qLogOutput(u'v_compute_: → ' + filename2)
                                        filename1=qPathPhoto + stamp + '.detect.jpg'
                                        filename2=qPathRec   + stamp + '.detect.jpg'
                                        if (not os.path.exists(filename1)) and (not os.path.exists(filename2)):
                                            try:
                                                cv2.imwrite(filename1, image_img)
                                                cv2.imwrite(filename2, image_img)
                                            except:
                                                pass

                    if (hit_count1 > 0):
                        cn_s.put(['DETECT1', hit_img1.copy()])
                        res_put = True
                    if (hit_count2 > 0):
                        cn_s.put(['DETECT2', hit_img2.copy()])
                        res_put = True
                    if (hit_count > 0):
                        cn_s.put(['DETECT', proc_img.copy()])
                        res_put = True

                if (res_put != True):
                    cn_s.put(['OK', ''])

        compute_busy = False
        if (cn_r.qsize() == 0):
            time.sleep(1.00)
        else:
            time.sleep(0.50)

    qLogOutput('v_compute_:terminate')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('v_compute_:end')



def drawTextImage(texts, drawWidth=480):
    global qFONT_default
    global qFONT_zh
    global qFONT_ko

    font18_default  = ImageFont.truetype(qFONT_default['file'], 18, encoding='unic')
    font18_defaulty =                    qFONT_default['offset']
    if (os.path.exists(qFONT_zh['file'])):
        font18_zh  = ImageFont.truetype(qFONT_zh['file']     , 18, encoding='unic')
        font18_zhy =                    qFONT_zh['offset']
    else:
        font18_zh  = ImageFont.truetype(qFONT_default['file'], 18, encoding='unic')
        font18_zhy =                    qFONT_default['offset']
    if (os.path.exists(qFONT_ko['file'])):
        font18_ko  = ImageFont.truetype(qFONT_ko['file']     , 18, encoding='unic')
        font18_koy =                    qFONT_ko['offset']
    else:
        font18_ko  = ImageFont.truetype(qFONT_default['file'], 18, encoding='unic')
        font18_koy =                    qFONT_default['offset']

    maxlen = 0
    for i in range(0, len(texts)):
        if (texts[i][2:3] != ','):
                 lenstr = len(texts[i]) * 2
                 if (maxlen < lenstr):
                      maxlen = lenstr
        else:
            if   (texts[i][:3] == 'ja,') \
             or  (texts[i][:3] == 'zh,') \
             or  (texts[i][:3] == 'ko,'):
                 lenstr = len(texts[i]) * 2
                 if (maxlen < lenstr):
                      maxlen = lenstr
            else:
                 lenstr = len(texts[i])
                 if (maxlen < lenstr):
                      maxlen = lenstr

    if (drawWidth != 0):
        text_img  = Image.new('RGB', (drawWidth,10+30*len(texts)), (0xff, 0xff, 0xff))
        text_draw = ImageDraw.Draw(text_img)
    else:
        text_img  = Image.new('RGB', (50+9*maxlen,10+30*len(texts)), (0xff, 0xff, 0xff))
        text_draw = ImageDraw.Draw(text_img)

    for i in range(0, len(texts)):
        if (texts[i][2:3] != ','):
                text_draw.text((5, 30*i + font18_defaulty), texts[i], font=font18_default, fill=(0x00, 0x00, 0x00))
        else:
            if   (texts[i][:3] == 'zh,'):
                text_draw.text((5, 30*i + font18_zhy), texts[i], font=font18_zh, fill=(0x00, 0x00, 0x00))
            elif (texts[i][:3] == 'ko,'):
                text_draw.text((5, 30*i + font18_koy), texts[i], font=font18_ko, fill=(0x00, 0x00, 0x00))
            else:
                text_draw.text((5, 30*i + font18_defaulty), texts[i], font=font18_default, fill=(0x00, 0x00, 0x00))

    return np.asarray(text_img)

speech_start = 0
speech_beat  = 0
speech_busy  = False
speech_last  = 0
speech_seq   = 0
def proc_speech(cn_r, cn_s, ):
    global qBusyCtrl
    global qBusyInput
    global qBusySTT
    global qBusyTTS
    global qBusyPlay

    global qCtrlResultCV
    global qCtrlResultOCR
    global qCtrlResultTrn
    global qCtrlVision
    global qCtrlRecognize
    global qCtrlTranslate
  
    global speech_start
    global speech_beat
    global speech_busy
    global speech_last
    global speech_seq

    qLogOutput('v_speech__:init')

    runMode   = cn_r.get()
    cam1Dev   = cn_r.get()
    dspMode   = cn_r.get()
    dspWidth,dspHeight = qGetResolution(dspMode)
    cn_r.task_done()

    qLogOutput('v_speech__:runMode   =' + str(runMode   ))
    qLogOutput('v_speech__:cam1Dev   =' + str(cam1Dev   ))
    qLogOutput('v_speech__:dspMode   =' + str(dspMode   ))
    qLogOutput('v_speech__:dspWidth  =' + str(dspWidth  ))
    qLogOutput('v_speech__:dspHeight =' + str(dspHeight ))

    if (os.path.exists(qCtrlRecognize)):
        try:
            os.remove(qCtrlRecognize)
        except:
            pass

    if (os.path.exists(qCtrlTranslate)):
        try:
            os.remove(qCtrlTranslate)
        except:
            pass

    qLogOutput('v_speech__:start')
    speech_start = time.time()

    wBusyChange = False
    wBusyCtrl   = ''
    wBusyInput  = ''
    wBusySTT    = ''
    wBusyTTS    = ''
    wBusyPlay   = ''

    while (True):
        speech_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('v_speech__:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qLogOutput('v_speech__: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                cn_s.put(['PASS', ''])

            else:
                speech_busy = True
                res_put = False

                # 制御情報
                file=qCtrlVision
                temp=file.replace('.txt', '.tmp')
                if (os.path.exists(temp)):
                    try:
                        os.remove(temp)
                    except:
                        pass
                if (os.path.exists(file)) and (not os.path.exists(temp)):
                    inpText = ''
                    try:
                        os.rename(file, temp)
                        rt = codecs.open(temp, 'r', 'shift_jis')
                        for t in rt:
                            inpText = (inpText + ' ' + str(t)).strip()
                        rt.close
                        rt = None
                    except:
                        pass
                    # 終了
                    if (inpText == '_close_'):
                        cn_s.put(['END', ''])
                        time.sleep( 5.00)
                        res_put = True
                        break
                    # シャッター
                    if (inpText == '_shutter_'):
                        cn_s.put(['SHUTTER', ''])
                        res_put = True
                    # ズームイン
                    if (inpText == '_zoom_in_'):
                        cn_s.put(['ZOOMIN', ''])
                        res_put = True
                    # ズームアウト
                    if (inpText == '_zoom_out_'):
                        cn_s.put(['ZOOMOUT', ''])
                        res_put = True

                # 実行状況確認
                wBusyChange = False
                check = qBusyCheck(qBusyCtrl, 0)
                if (check != wBusyCtrl):
                    wBusyCtrl   = check
                    wBusyChange = True
                check = qBusyCheck(qBusyInput, 0)
                if (check != wBusyInput):
                    wBusyInput  = check
                    wBusyChange = True
                check = qBusyCheck(qBusySTT, 0)
                if (check != wBusySTT):
                    wBusySTT    = check
                    wBusyChange = True
                check = qBusyCheck(qBusyTTS, 0)
                if (check != wBusyTTS):
                    wBusyTTS    = check
                    wBusyChange = True
                check = qBusyCheck(qBusyPlay, 0)
                if (check != wBusyPlay):
                    wBusyPlay   = check
                    wBusyChange = True
                # 文字列を描画する
                if (wBusyChange == True):
                    texts=[]
                    texts.append('[Speech Status]')
                    if (wBusyCtrl == 'busy'):
                        texts.append(' Ctrl  : Busy!_')
                    else:
                        texts.append(' Ctrl  : ______')
                    if (wBusyInput == 'busy'):
                        texts.append(' Input : Ready_')
                    else:
                        texts.append(' Input : ______')
                    if (wBusySTT == 'busy'):
                        texts.append(' STT   : Busy!_')
                    else:
                        texts.append(' STT   : ______')
                    if (wBusyTTS == 'busy'):
                        texts.append(' TTS   : Busy!_')
                    else:
                        texts.append(' TTS   : ______')
                    if (wBusyPlay == 'busy'):
                        texts.append(' Play  : Busy!_')
                    else:
                        texts.append(' Play  : ______')

                    text_img = drawTextImage(texts, 150)
                    cn_s.put(['STATUS', text_img.copy()])
                    res_put = True

                # CV結果
                file=qCtrlResultCV
                temp=file.replace('.txt', '.tmp')
                if (os.path.exists(temp)):
                    try:
                        os.remove(temp)
                    except:
                        pass
                if (os.path.exists(file)) and (not os.path.exists(temp)):
                    texts=[]
                    try:
                        os.rename(file, temp)
                        rt = codecs.open(temp, 'r', 'utf-8')
                        for t in rt:
                            t = str(t).strip()
                            if (t != ''):
                                texts.append(t)
                        rt.close
                        rt = None
                    except:
                        pass
                    # 文字列を描画する
                    if (len(texts) >= 1):
                        text_img = drawTextImage(texts, int(dspWidth * 0.4))
                        cn_s.put(['CV', text_img.copy()])
                        res_put = True

                # OCR結果
                file=qCtrlResultOCR
                temp=file.replace('.txt', '.tmp')
                if (os.path.exists(temp)):
                    try:
                        os.remove(temp)
                    except:
                        pass
                if (os.path.exists(file)) and (not os.path.exists(temp)):
                    texts=[]
                    try:
                        os.rename(file, temp)
                        rt = codecs.open(temp, 'r', 'utf-8')
                        for t in rt:
                            t = str(t).strip()
                            if (t != ''):
                                texts.append(t)
                        rt.close
                        rt = None
                    except:
                        pass
                    # 文字列を描画する
                    if (len(texts) >= 1):
                        text_img = drawTextImage(texts, int(dspWidth * 0.4))
                        cn_s.put(['OCR', text_img.copy()])
                        res_put = True

                # OCR翻訳結果
                file=qCtrlResultTrn
                temp=file.replace('.txt', '.tmp')
                if (os.path.exists(temp)):
                    try:
                        os.remove(temp)
                    except:
                        pass
                if (os.path.exists(file)) and (not os.path.exists(temp)):
                    texts=[]
                    try:
                        os.rename(file, temp)
                        rt = codecs.open(temp, 'r', 'utf-8')
                        for t in rt:
                            t = str(t).strip()
                            if (t != ''):
                                texts.append(t)
                        rt.close
                        rt = None
                    except:
                        pass
                    # 文字列を描画する
                    if (len(texts) >= 1):
                        text_img = drawTextImage(texts, int(dspWidth * 0.4))
                        cn_s.put(['TRN', text_img.copy()])
                        res_put = True

                # 音声認識結果
                file=qCtrlRecognize
                temp=file.replace('.txt', '.tmp')
                if (os.path.exists(temp)):
                    try:
                        os.remove(temp)
                    except:
                        pass
                if (os.path.exists(file)) and (not os.path.exists(temp)):
                    texts=[]
                    try:
                        os.rename(file, temp)
                        rt = codecs.open(temp, 'r', 'utf-8')
                        for t in rt:
                            t = str(t).strip()
                            if (t != ''):
                                texts.append(t)
                        rt.close
                        rt = None
                    except:
                        pass
                    # 文字列を描画する
                    if (len(texts) >= 1):
                        text_img = drawTextImage(texts, int(dspWidth * 0))  #0.5->0
                        cn_s.put(['RECOGNIZE', text_img.copy()])
                        res_put = True

                # 機械翻訳結果
                file=qCtrlTranslate
                temp=file.replace('.txt', '.tmp')
                if (os.path.exists(temp)):
                    try:
                        os.remove(temp)
                    except:
                        pass
                if (os.path.exists(file)) and (not os.path.exists(temp)):
                    texts=[]
                    try:
                        os.rename(file, temp)
                        rt = codecs.open(temp, 'r', 'utf-8')
                        for t in rt:
                            t = str(t).strip()
                            if (t != ''):
                                texts.append(t)
                        rt.close
                        rt = None
                    except:
                        pass
                    # 文字列を描画する
                    if (len(texts) >= 1):
                        text_img = drawTextImage(texts, int(dspWidth * 0))  #0.5->0
                        cn_s.put(['TRANSLATE', text_img.copy()])
                        res_put = True

                if (res_put != True):
                    cn_s.put(['OK', ''])

        speech_busy = False
        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.05)

    qLogOutput('v_speech__:terminate')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('v_speech__:end')



output_start = 0
output_beat  = 0
output_busy  = False
output_last  = 0
output_seq   = 0
def proc_output(cn_r, cn_s, ):
    global inp1_Height
    global inp1_Width
    global inp1_Image
    global inp1_FPS
    global inp2_FPS

    global DisplayEvent, MousePointX, MousePointY

    global output_start
    global output_beat
    global output_busy
    global output_last
    global output_seq

    qLogOutput('video_out_:init')

    runMode    = cn_r.get()
    cam1Dev    = cn_r.get()
    cam1Rotate = int(cn_r.get())
    dspMode    = cn_r.get()
    dspWidth,dspHeight = qGetResolution(dspMode)
    cn_r.task_done()

    qLogOutput('video_out_:runMode   =' + str(runMode   ))
    qLogOutput('video_out_:cam1Dev   =' + str(cam1Dev   ))
    qLogOutput('video_out_:cam1Rotate=' + str(cam1Rotate))
    qLogOutput('video_out_:dspMode   =' + str(dspMode   ))
    qLogOutput('video_out_:dspWidth  =' + str(dspWidth  ))
    qLogOutput('video_out_:dspHeight =' + str(dspHeight ))

    blue_img = np.zeros((240,320,3), np.uint8)
    cv2.rectangle(blue_img,(0,0),(320,240),(255,0,0),-1)
    cv2.putText(blue_img, 'No Image !', (40,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
    display_img = cv2.resize(blue_img, (dspWidth, dspHeight ))

    input_img1     = display_img.copy()
    input_img2     = None

    detect1_img    = None
    detect1_time   = time.time()
    detect2_img    = None
    detect2_time   = time.time()
    detect_img     = None
    detect_time    = time.time()
    status_img     = None
    status_time    = time.time()
    visionCV_img   = None
    visionCV_time  = time.time()
    visionOCR_img  = None
    visionOCR_time = time.time()
    visionTrn_img  = None
    visionTrn_time = time.time()
    disptext1_img  = None
    disptext1_time = time.time()
    disptext2_img  = None
    disptext2_time = time.time()
    disptext3_img  = None
    disptext3_time = time.time()
    disptext4_img  = None
    disptext4_time = time.time()
    disptext5_img  = None
    disptext5_time = time.time()
    disptext6_img  = None
    disptext6_time = time.time()

    qLogOutput('video_out_:start')
    output_start = time.time()

    fps_class = qFPS()
    while (True):
        output_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('video_out_:None=break')
                break

            #if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
            if (cn_r.qsize() > 3) or (cn_s.qsize() > 3):
                qLogOutput('video_out_: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                cn_s.put(['PASS', ''])

            else:
                output_busy = True

                if   (mode_get == 'DETECT1'):
                    detect1_img  = data_get.copy()
                    detect1_time = time.time()

                elif (mode_get == 'DETECT2'):
                    detect2_img  = data_get.copy()
                    detect2_time = time.time()

                elif (mode_get == 'DETECT'):
                    detect_img  = data_get.copy()
                    detect_time = time.time()

                elif (mode_get == 'STATUS'):
                    status_img  = data_get.copy()
                    status_time = time.time()

                elif (mode_get == 'CV'):
                    visionCV_img  = data_get.copy()
                    visionCV_time = time.time()

                elif (mode_get == 'OCR'):
                    visionOCR_img  = data_get.copy()
                    visionOCR_time = time.time()

                elif (mode_get == 'TRN'):
                    visionTrn_img  = data_get.copy()
                    visionTrn_time = time.time()

                elif (mode_get == 'RECOGNIZE'):
                    disptext6_img  = disptext5_img
                    disptext6_time = disptext5_time
                    disptext5_img  = disptext4_img
                    disptext5_time = disptext4_time
                    disptext4_img  = disptext3_img
                    disptext4_time = disptext3_time
                    disptext3_img  = disptext2_img
                    disptext3_time = disptext2_time
                    disptext2_img  = disptext1_img
                    disptext2_time = disptext1_time
                    disptext1_img  = data_get.copy()
                    disptext1_time = time.time()

                elif (mode_get == 'TRANSLATE'):
                    disptext6_img  = disptext5_img
                    disptext6_time = disptext5_time
                    disptext5_img  = disptext4_img
                    disptext5_time = disptext4_time
                    disptext4_img  = disptext3_img
                    disptext4_time = disptext3_time
                    disptext3_img  = disptext2_img
                    disptext3_time = disptext2_time
                    disptext2_img  = disptext1_img
                    disptext2_time = disptext1_time
                    disptext1_img  = data_get.copy()
                    disptext1_time = time.time()

                elif (mode_get == 'INPUT2'):
                    input_img2 = data_get.copy()

                elif (mode_get == 'INPUT'):
                    input_img1 = data_get.copy()
                    input_height, input_width = input_img1.shape[:2]
                    inp_fps = 'Inp: {:.1f}'.format(inp1_FPS) + 'fps'
                    inp_src = str(inp1_Width) + 'x' + str(inp1_Height)
                    if (inp1_Zoom != '1.0'):
                        inp_src += ' (Zoom ' + inp1_Zoom + ')'
                    out_fps = 'Out: {:.1f}'.format(fps_class.get()) + 'fps'
                    out_src = str(dspWidth) + 'x' + str(dspHeight)

                    display_img = cv2.resize(input_img1, (dspWidth, dspHeight))
                    if (abs(int(cam1Rotate)) == 360):
                        display_img = cv2.flip(display_img,1) # Mirror image
                    cv2.putText(display_img, inp_fps, ( 20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                    cv2.putText(display_img, inp_src, (180,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))
                    cv2.putText(display_img, out_fps, ( 20,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                    cv2.putText(display_img, out_src, (180,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))

                    if (os.name == 'nt'):
                        baseY = dspHeight - 50
                        baseX = 20
                    else:
                        baseY = dspHeight - 80
                        baseX = 20

                    # input_img2 overlay
                    if  (not input_img2 is None):
                        image_img   = input_img2.copy()
                        image_height, image_width = image_img.shape[:2]
                        inp2_fps = 'Inp: {:.1f}'.format(inp2_FPS) + 'fps'
                        inp2_src = str(inp2_Width) + 'x' + str(inp2_Height)
                        if (inp2_Zoom != '1.0'):
                            inp2_src += ' (Zoom ' + inp2_Zoom + ')'
                        cv2.putText(image_img, inp2_fps, ( 20,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                        cv2.putText(image_img, inp2_src, (180,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))
                        wrkWidth  = int(dspWidth * 0.25)
                        wrkHeight = int(wrkWidth * image_height / image_width)
                        overlay_img = cv2.resize(image_img, (wrkWidth, wrkHeight))
                        baseY -= wrkHeight
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = overlay_img
                                baseY = baseY - 20
                            except:
                                qLogOutput('vision_out: input_img2 overlay error!')

                    baseY = 90
                    baseX = int(dspWidth * 0.65)

                    # detect1 overlay
                    if  (not detect1_img is None) \
                    and (int(time.time() - detect1_time) <= 5):
                        image_img   = detect1_img.copy()
                        image_height, image_width = image_img.shape[:2]
                        wrkWidth  = int(dspWidth * 0.30)
                        wrkHeight = int(wrkWidth * image_height / image_width)
                        overlay_img = cv2.resize(image_img, (wrkWidth, wrkHeight))
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = overlay_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: detect1 overlay error!')

                    # detect2 overlay
                    if  (not detect2_img is None) \
                    and (int(time.time() - detect2_time) <= 5):
                        image_img   = detect2_img.copy()
                        image_height, image_width = image_img.shape[:2]
                        wrkWidth  = int(dspWidth * 0.30)
                        wrkHeight = int(wrkWidth * image_height / image_width)
                        overlay_img = cv2.resize(image_img, (wrkWidth, wrkHeight))
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = overlay_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: detect2 overlay error!')

                    baseY = 90
                    baseX = int(dspWidth * 0.05)

                    # disptext6 alpha blending
                    if  (not disptext6_img is None) \
                    and (int(time.time() - disptext6_time) <= 15):
                        wrkHeight, wrkWidth = disptext6_img.shape[:2]
                        while ((baseX + wrkWidth) >= dspWidth):
                            disptext1_img = cv2.resize(disptext1_img,(int(wrkWidth*0.7), wrkHeight))
                            wrkHeight, wrkWidth = disptext1_img.shape[:2]
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, disptext6_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: disptext6 alpha blending error!')

                    # disptext5 alpha blending
                    if  (not disptext5_img is None) \
                    and (int(time.time() - disptext5_time) <= 15):
                        wrkHeight, wrkWidth = disptext5_img.shape[:2]
                        while ((baseX + wrkWidth) >= dspWidth):
                            disptext1_img = cv2.resize(disptext1_img,(int(wrkWidth*0.7), wrkHeight))
                            wrkHeight, wrkWidth = disptext1_img.shape[:2]
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, disptext5_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: disptext5 alpha blending error!')

                    # disptext4 alpha blending
                    if  (not disptext4_img is None) \
                    and (int(time.time() - disptext4_time) <= 15):
                        wrkHeight, wrkWidth = disptext4_img.shape[:2]
                        while ((baseX + wrkWidth) >= dspWidth):
                            disptext1_img = cv2.resize(disptext1_img,(int(wrkWidth*0.7), wrkHeight))
                            wrkHeight, wrkWidth = disptext1_img.shape[:2]
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, disptext4_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: disptext4 alpha blending error!')

                    # disptext3 alpha blending
                    if  (not disptext3_img is None) \
                    and (int(time.time() - disptext3_time) <= 15):
                        wrkHeight, wrkWidth = disptext3_img.shape[:2]
                        while ((baseX + wrkWidth) >= dspWidth):
                            disptext1_img = cv2.resize(disptext1_img,(int(wrkWidth*0.7), wrkHeight))
                            wrkHeight, wrkWidth = disptext1_img.shape[:2]
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, disptext3_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: disptext3 alpha blending error!')

                    # disptext2 alpha blending
                    if  (not disptext2_img is None) \
                    and (int(time.time() - disptext2_time) <= 15):
                        wrkHeight, wrkWidth = disptext2_img.shape[:2]
                        while ((baseX + wrkWidth) >= dspWidth):
                            disptext1_img = cv2.resize(disptext1_img,(int(wrkWidth*0.7), wrkHeight))
                            wrkHeight, wrkWidth = disptext1_img.shape[:2]
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, disptext2_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: disptext2 alpha blending error!')

                    # disptext1 alpha blending
                    if  (not disptext1_img is None) \
                    and (int(time.time() - disptext1_time) <= 15):
                        wrkHeight, wrkWidth = disptext1_img.shape[:2]
                        while ((baseX + wrkWidth) >= dspWidth):
                            disptext1_img = cv2.resize(disptext1_img,(int(wrkWidth*0.7), wrkHeight))
                            wrkHeight, wrkWidth = disptext1_img.shape[:2]
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, disptext1_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: disptext1 alpha blending error!')

                    if (os.name == 'nt'):
                        baseY = dspHeight - 50
                        baseX = dspWidth - 20
                    else:
                        baseY = dspHeight - 80
                        baseX = dspWidth - 20

                    # status alpha blending
                    if  (not status_img is None) \
                    and (int(time.time() - status_time) <= 60):
                        wrkHeight, wrkWidth = status_img.shape[:2]
                        baseY -= wrkHeight
                        baseX -= wrkWidth
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, status_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY - 20
                            except:
                                qLogOutput('vision_out: status alpha blending error!')

                    baseY = 90
                    baseX = int(dspWidth * 0.58)

                    # visionOCR alpha blending
                    if  (not visionOCR_img is None) \
                    and (int(time.time() - visionOCR_time) <= 15):
                        wrkHeight, wrkWidth = visionOCR_img.shape[:2]
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, visionOCR_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: visionOCR alpha blending error!')

                    # visionTrn alpha blending
                    if  (not visionTrn_img is None) \
                    and (int(time.time() - visionTrn_time) <= 30):
                        wrkHeight, wrkWidth = visionTrn_img.shape[:2]
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, visionTrn_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: visionTrn alpha blending error!')

                    # visionCV alpha blending
                    if  (not visionCV_img is None) \
                    and (int(time.time() - visionCV_time) <= 40):
                        wrkHeight, wrkWidth = visionCV_img.shape[:2]
                        if ((baseY+wrkHeight) < dspHeight):
                            try:
                                src_img=display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth]
                                alpha_img= cv2.addWeighted(src_img, 0.4, visionCV_img, 0.6, 0.0)
                                display_img[baseY:baseY+wrkHeight, baseX:baseX+wrkWidth] = alpha_img
                                baseY = baseY+wrkHeight + 20
                            except:
                                qLogOutput('vision_out: visionCV alpha blending error!')

                if (display_img is None):
                    cn_s.put(['OK', ''])
                else:
                    cn_s.put(['DISPLAY', display_img.copy()])

        output_busy = False
        if (cn_r.qsize() == 0):
            time.sleep(0.05)
        else:
            time.sleep(0.01)

    qLogOutput('video_out_:terminate')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('video_out_:end')



DisplayEvent = None
MousePointX  = None
MousePointY  = None
def DisplayMouseEvent(event, x, y, flags, param):
    global DisplayEvent, MousePointX, MousePointY
    if (event == cv2.EVENT_LBUTTONUP):
        DisplayEvent = cv2.EVENT_LBUTTONUP
        MousePointX  = x
        MousePointY  = y
        #qLogOutput('EVENT_LBUTTONUP')
    elif (event == cv2.EVENT_RBUTTONDOWN):
        DisplayEvent = cv2.EVENT_RBUTTONDOWN
        MousePointX  = x
        MousePointY  = y
        #qLogOutput('EVENT_RBUTTONDOWN')



def main_cv(seq, fileId, runMode, cam1Dev, inpFile, sync=False):
    global qPathCv
    global qPathRec
    global qPathWork

    if (True):
        inpCV  = inpFile
        tmpCV  = qPathWork  + 'temp_cv.' + seq + '.jpg'
        outCV  = qPathCv    + fileId + '.cv.' + qLangCV + '.txt'
        inpOCR = inpFile
        tmpOCR = qPathWork  + 'temp_ocr.' + seq + '.jpg'
        outOCR = qPathCv    + fileId + '.ocr.' + qLangOCR + '.txt'
        outTrn = qPathCv    + fileId + '.ocr.' + qLangTrn + '.txt'

    if (True):
        api = subprocess.Popen(['python', '_vision_v3_all_api.py', \
              runMode, cam1Dev, qApiCV, qApiOCR, qApiTrn, qLangCV, qLangOCR, qLangTrn, \
              str(seq), fileId, inpCV, tmpCV, outCV, inpOCR, tmpOCR, outOCR, outTrn, ], \
              )
        if (sync == True):
            api.wait()
            api.terminate()
            api = None



def main_init(runMode, cam1Dev, ):
    global qPathDetect
    global qPathPhoto
    global qPathCv
    global qPathRec
    global qPathWork

    qMakeDirs('temp/_log/',   False)

    if (cam1Dev.isdigit()):
        qMakeDirs(qPathDetect, True )
        qMakeDirs(qPathPhoto,  True )
        qMakeDirs(qPathCv,     True )
        qMakeDirs(qPathRec,    False)
        qMakeDirs(qPathWork,   True )
    else:
        qMakeDirs(qPathDetect, True )
        qMakeDirs(qPathPhoto,  True )
        qMakeDirs(qPathCv,     True )
        qMakeDirs(qPathRec,    True )
        qMakeDirs(qPathWork,   True )



main_start = 0
main_beat  = 0
main_busy  = False
main_last  = 0
main_seq   = 0
if (__name__ == '__main__'):
    #global main_beat

    qLogOutput('')
    qLogOutput('video_main:init')
    qLogOutput('video_main:exsample.py runMode, cam... ')
    #runMode  debug,
    #cam1Dev num or file

    runMode  = 'handsfree'

    cam1Dev  = '9'
    cam1Rote = '0'
    #cam1Mode = 'full'
    cam1Mode = '1280x720'
    cam1Zoom = '1.0'
    chk = False
    while (chk == False) and (cam1Dev > '0'):
        try:
            dev = cv2.VideoCapture(int(cam1Dev))
            ret, frame = dev.read()
            if ret == True:
                dev.release()
                chk = True
            else:
                cam1Dev = str(int(cam1Dev)-1)
        except:
            cam1Dev = str(int(cam1Dev)-1)
    if (cam1Dev == '0'):
        cam1Mode = 'vga'

    if (cam1Dev > '0'):
        cam2Dev  = '0'
        cam2Rote = '0'
        cam2Mode = 'vga'
        cam2Zoom = '1.0'
    else:
        cam2Dev  = 'none'
        cam2Rote = '0'
        cam2Mode = 'vga'
        cam2Zoom = '1.0'

    # 20190303 Demo mode
    cam2Dev  = 'none'
    cam2Rote = '0'
    cam2Mode = 'vga'
    cam2Zoom = '1.0' 
 
    dspMode  = 'half'
    if (os.name == 'nt'):
        dspMode  = '1280x720'

    casName1  = 'face'
    casName2  = 'cars'

    autoShot  = '0'

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
        autoShot = '0'
        if (runMode=='debug'):
            autoShot = '60'
        elif (runMode=='knowledge'):
            autoShot = '10'
            cam2Dev = 'none'

    if (len(sys.argv) >= 3):
        cam1Dev  = str(sys.argv[2])
    if (len(sys.argv) >= 4):
        cam1Rote = str(sys.argv[3]).lower()
    if (len(sys.argv) >= 5):
        val = str(sys.argv[4]).lower()
        if (val != 'default') and (val != 'auto'):
            cam1Mode = val
    if (len(sys.argv) >= 6):
        cam1Zoom = str(sys.argv[5]).lower()
    if (len(sys.argv) >= 7):
        cam2Dev  = str(sys.argv[6])
    if (len(sys.argv) >= 8):
        cam2Rote = str(sys.argv[7]).lower()
    if (len(sys.argv) >= 9):
        cam2Zoom = str(sys.argv[8]).lower()
    if (len(sys.argv) >= 10):
        val = str(sys.argv[9]).lower()
        if (val != 'default') and (val != 'auto'):
            cam2Mode = val

    if (len(sys.argv) >= 11):
        val = str(sys.argv[10]).lower()
        if (val != 'default') and (val != 'auto'):
            dspMode = val

    if (len(sys.argv) >= 12):
        casName1 = str(sys.argv[11])
    if (len(sys.argv) >= 13):
        casname2 = str(sys.argv[12])
    if (len(sys.argv) >= 14):
        qApiCV   = str(sys.argv[13]).lower()
        qApiOCR  = qApiCV
        qApiTrn  = qApiCV
    if (len(sys.argv) >= 15):
        qApiOCR  = str(sys.argv[14]).lower()
    if (len(sys.argv) >= 16):
        qApiTrn  = str(sys.argv[15]).lower()
    if (len(sys.argv) >= 17):
        qLangCV  = str(sys.argv[16]).lower()
        qLangOCR = qLangCV
    if (len(sys.argv) >= 18):
        qLangOCR = str(sys.argv[17]).lower()
    if (len(sys.argv) >= 19):
        qLangTrn = str(sys.argv[18]).lower()

    if (len(sys.argv) >= 20):
        autoShot = str(sys.argv[19]).lower()

    if (casName1 != 'none'):
        if (casName1 == 'cars'):
            casName1 = '_vision_opencv_cars.xml'
        if (casName1 == 'face'):
            casName1 = '_vision_opencv_face.xml'
        if (casName1 == 'fullbody'):
            casName1 = '_vision_opencv_fullbody.xml'

    if (casName2 != 'none'):
        if (casName2 == 'cars'):
            casName2 = '_vision_opencv_cars.xml'
        if (casName2 == 'face'):
            casName2 = '_vision_opencv_face.xml'
        if (casName2 == 'fullbody'):
            casName2 = '_vision_opencv_fullbody.xml'

    qLogOutput('')
    qLogOutput('video_main:runMode  =' + str(runMode  ))
    qLogOutput('video_main:cam1Dev  =' + str(cam1Dev  ))
    qLogOutput('video_main:cam1Rote =' + str(cam1Rote ))
    qLogOutput('video_main:cam1Mode =' + str(cam1Mode ))
    qLogOutput('video_main:cam1Zoom =' + str(cam1Zoom ))
    qLogOutput('video_main:cam2Dev  =' + str(cam2Dev  ))
    qLogOutput('video_main:cam2Rote =' + str(cam2Rote ))
    qLogOutput('video_main:cam2Mode =' + str(cam2Mode ))
    qLogOutput('video_main:cam2Zoom =' + str(cam2Zoom ))
    qLogOutput('video_main:dspMode  =' + str(dspMode  ))

    qLogOutput('video_main:casName1 =' + str(casName1 ))
    qLogOutput('video_main:casName2 =' + str(casName2 ))
    qLogOutput('video_main:qApiCV   =' + str(qApiCV   ))
    qLogOutput('video_main:qApiOCR  =' + str(qApiOCR  ))
    qLogOutput('video_main:qApiTrn  =' + str(qApiTrn  ))
    qLogOutput('video_main:qLangCV  =' + str(qLangCV  ))
    qLogOutput('video_main:qLangOCR =' + str(qLangOCR ))
    qLogOutput('video_main:qLangTrn =' + str(qLangTrn ))

    qLogOutput('video_main:autoShot =' + str(autoShot ))

    main_init(runMode, cam1Dev, )

    qLogOutput('')
    qLogOutput('video_main:start')
    main_start   = time.time()
    main_beat    = 0
    window_onece = True

    wrkText = u'画像制御機能が起動しました。'
    tts_speech(runMode, 'vision.00', wrkText, )

    shutter_flag = False
    shutter_last = time.time()

    inp1_s       = queue.Queue()
    inp1_r       = queue.Queue()
    inp1_proc    = None
    inp1_beat    = 0
    inp1_pass    = 0

    inp2_s       = queue.Queue()
    inp2_r       = queue.Queue()
    inp2_proc    = None
    inp2_beat    = 0
    inp2_pass    = 0

    compute_s    = queue.Queue()
    compute_r    = queue.Queue()
    compute_proc = None
    compute_beat = 0
    compute_pass = 0

    speech_s     = queue.Queue()
    speech_r     = queue.Queue()
    speech_proc  = None
    speech_beat  = 0
    speech_pass  = 0

    output_s     = queue.Queue()
    output_r     = queue.Queue()
    output_proc  = None
    output_beat  = 0
    output_pass  = 0

    while (True):
        main_beat = time.time()

        # Thread timeout check

        if (inp1_beat != 0):
          if (cam1Dev.isdigit()):
            sec = int(time.time() - inp1_beat)
            if (sec > 60):
                qLogOutput('video_main:inp1_proc 60s')
                qLogOutput('video_main:inp1_proc break')
                inp1_s.put([None, None])
                time.sleep(3.00)
                inp1_proc = None
                inp1_beat = 0
                inp1_pass = 0

        if (inp2_beat != 0):
          if (cam2Dev.isdigit()):
            sec = int(time.time() - inp2_beat)
            if (sec > 60):
                qLogOutput('video_main:inp2_proc 60s')
                qLogOutput('video_main:inp2_proc break')
                inp2_s.put([None, None])
                time.sleep(3.00)
                inp2_proc = None
                inp2_beat = 0
                inp2_pass = 0

        if (compute_beat != 0):
            sec = int(time.time() - compute_beat)
            if (sec > 60):
                qLogOutput('video_main:compute_proc 60s')
                qLogOutput('video_main:compute_proc break')
                compute_s.put([None, None])
                time.sleep(3.00)
                compute_proc = None
                compute_beat = 0
                compute_pass = 0

        if (speech_beat != 0):
            sec = int(time.time() - speech_beat)
            if (sec > 60):
                qLogOutput('video_main:speech_proc 60s')
                qLogOutput('video_main:speech_proc break')
                speech_s.put([None, None])
                time.sleep(3.00)
                speech_proc = None
                speech_beat = 0
                speech_pass = 0

        if (output_beat != 0):
          if (cam1Dev.isdigit()):
            sec = int(time.time() - output_beat)
            if (sec > 60):
                qLogOutput('video_main:output_proc 60s')
                qLogOutput('video_main:output_proc break')
                output_s.put([None, None])
                time.sleep(3.00)
                output_proc = None
                output_beat = 0
                output_pass = 0

        # Thread start

        if (inp1_proc is None) and (cam1Dev != 'none'):
            while (inp1_s.qsize() > 0):
                dummy = inp1_s.get()
            while (inp1_r.qsize() > 0):
                dummy = inp1_r.get()
            inp1_proc = threading.Thread(target=proc_inp1, args=(inp1_s,inp1_r,))
            inp1_proc.daemon = True
            inp1_s.put(runMode  )
            inp1_s.put(cam1Dev  )
            inp1_s.put(cam1Rote )
            inp1_s.put(cam1Mode )
            inp1_s.put(cam1Zoom )
            inp1_s.put(dspMode  )
            inp1_proc.start()
            time.sleep(1.00)

            inp1_s.put(['START', ''])

        if (inp2_proc is None) and (cam2Dev != 'None'):
            while (inp2_s.qsize() > 0):
                dummy = inp2_s.get()
            while (inp2_r.qsize() > 0):
                dummy = inp2_r.get()
            inp2_proc = threading.Thread(target=proc_inp2, args=(inp2_s,inp2_r,))
            inp2_proc.daemon = True
            inp2_s.put(runMode  )
            inp2_s.put(cam2Dev  )
            inp2_s.put(cam2Rote )
            inp2_s.put(cam2Mode )
            inp2_s.put(cam2Zoom )
            inp2_proc.start()
            time.sleep(1.00)

            inp2_s.put(['START', ''])

        if (compute_proc is None):
            while (compute_s.qsize() > 0):
                dummy = compute_s.get()
            while (compute_r.qsize() > 0):
                dummy = compute_r.get()
            compute_proc = threading.Thread(target=proc_compute, args=(compute_s,compute_r,))
            compute_proc.daemon = True
            compute_s.put(runMode )
            compute_s.put(cam1Dev)
            compute_s.put(casName1)
            compute_s.put(casName2)
            compute_proc.start()
            time.sleep(1.00)

            compute_s.put(['START', ''])

        if (speech_proc is None):
            while (speech_s.qsize() > 0):
                dummy = speech_s.get()
            while (speech_r.qsize() > 0):
                dummy = speech_r.get()
            speech_proc = threading.Thread(target=proc_speech, args=(speech_s,speech_r,))
            speech_proc.daemon = True
            speech_s.put(runMode )
            speech_s.put(cam1Dev)
            speech_s.put(dspMode )
            speech_proc.start()
            time.sleep(1.00)

            speech_s.put(['START', ''])

        if (output_proc is None):
            while (output_s.qsize() > 0):
                dummy = output_s.get()
            while (output_r.qsize() > 0):
                dummy = output_r.get()
            output_proc = threading.Thread(target=proc_output, args=(output_s,output_r,))
            output_proc.daemon = True
            output_s.put(runMode  )
            output_s.put(cam1Dev )
            output_s.put(cam1Rote)
            output_s.put(dspMode  )
            output_proc.start()
            time.sleep(1.00)

            output_s.put(['START', ''])

        # processing

        if (int(autoShot) > 0):
            sec = int(time.time() - shutter_last)
            if (sec > int(autoShot)):
                shutter_flag = True

                sec = int(time.time() - main_start)
                if (sec > 600):
                    autoShot = 3600

        if (inp1_r.qsize() == 0 and inp1_s.qsize() == 0):
            inp1_s.put(['PROC', ''])
            inp1_pass += 1
        else:
            inp1_pass = 0
        if (inp1_pass > 50):
            inp1_s.put(['PASS', ''])
            inp1_pass = 0

        break_flag = False
        while (inp1_r.qsize() > 0):
            inp1_get = inp1_r.get()
            inp1_res = inp1_get[0]
            inp1_dat = inp1_get[1]
            inp1_r.task_done()
            if (inp1_res == 'IMAGE'):
                inp1_img = inp1_dat.copy()
                if (compute_s.qsize() == 0):
                    compute_s.put(['INPUT', inp1_img.copy()])
                if (output_s.qsize() == 0):
                    output_s.put(['INPUT', inp1_img.copy()])

            if (inp1_res == 'END'):
                break_flag = True
            if (inp1_res == 'ERROR'):
                break_flag = True
        if (break_flag == True):
            break

        if (inp2_r.qsize() == 0 and inp2_s.qsize() == 0):
            inp2_s.put(['PROC', ''])
            inp2_pass += 1
        else:
            inp2_pass = 0
        if (inp2_pass > 50):
            inp2_s.put(['PASS', ''])
            inp2_pass = 0

        while (inp2_r.qsize() > 0):
            inp2_get = inp2_r.get()
            inp2_res = inp2_get[0]
            inp2_dat = inp2_get[1]
            inp2_r.task_done()
            if (inp2_res == 'IMAGE'):
                inp2_img = inp2_dat.copy()
                if (output_s.qsize() == 0):
                    output_s.put(['INPUT2', inp2_img.copy()])

        if (compute_r.qsize() == 0 and compute_s.qsize() == 0):
            compute_s.put(['PROC', ''])
            compute_pass += 1
        else:
            compute_pass = 0
        if (compute_pass > 50):
            compute_s.put(['PASS', ''])
            compute_pass = 0

        while (compute_r.qsize() > 0):
            compute_get = compute_r.get()
            compute_res = compute_get[0]
            compute_dat = compute_get[1]
            compute_r.task_done()

            if (compute_res == 'DETECT1'):
                output_s.put([ 'DETECT1', compute_dat.copy()])
            if (compute_res == 'DETECT2'):
                output_s.put([ 'DETECT2', compute_dat.copy()])
            if (compute_res == 'DETECT'):
                output_s.put([ 'DETECT' , compute_dat.copy()])

        if (speech_r.qsize() == 0 and speech_s.qsize() == 0):
            speech_s.put(['PROC', ''])
            speech_pass += 1
        else:
            speech_pass = 0
        if (speech_pass > 50):
            speech_s.put(['PASS', ''])
            speech_pass = 0

        break_flag = False
        while (speech_r.qsize() > 0):
            speech_get = speech_r.get()
            speech_res = speech_get[0]
            speech_dat = speech_get[1]
            speech_r.task_done()

            if (speech_res == 'END'):
                break_flag = True
            if (speech_res == 'ERROR'):
                break_flag = True

            if (speech_res == 'SHUTTER'):
                shutter_flag = True

            if (speech_res == 'ZOOMIN'):
                cam1Zoom = '{:.1f}'.format(float(cam1Zoom) + 0.5)
                inp1_s.put(['ZOOM', cam1Zoom])
                #cam2Zoom = '{:.1f}'.format(float(cam2Zoom) + 0.5)
                #inp2_s.put(['ZOOM', cam2Zoom])

            if (speech_res == 'ZOOMOUT'):
                cam1Zoom = '1.0'
                inp1_s.put(['ZOOM', cam1Zoom])
                cam2Zoom = '1.0'
                inp2_s.put(['ZOOM', cam2Zoom])

            if (speech_res == 'STATUS'):
                output_s.put(['STATUS', speech_dat.copy()])

            if (speech_res == 'CV'):
                output_s.put(['CV', speech_dat.copy()])

            if (speech_res == 'OCR'):
                output_s.put(['OCR', speech_dat.copy()])

            if (speech_res == 'TRN'):
                output_s.put(['TRN', speech_dat.copy()])

            if (speech_res == 'RECOGNIZE'):
                output_s.put(['RECOGNIZE', speech_dat.copy()])

            if (speech_res == 'TRANSLATE'):
                output_s.put(['TRANSLATE', speech_dat.copy()])

        if (break_flag == True):
            break

        if (output_r.qsize() == 0 and output_s.qsize() == 0):
            output_s.put(['PROC', ''])
            output_pass += 1
        else:
            output_pass = 0
        if (output_pass > 50):
            output_s.put(['PASS', ''])
            output_pass = 0

        while (output_r.qsize() > 0):
            output_get = output_r.get()
            output_res = output_get[0]
            output_dat = output_get[1]
            output_r.task_done()

            if (output_res == 'DISPLAY'):
                display_img = output_dat.copy()
                dspHeight, dspWidth = display_img.shape[:2]

                # display_img
                #cv2.putText(display_img, 'CANCEL', (40,dspHeight-100), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255))
                #cv2.rectangle(display_img,(35,dspHeight-95),(300,dspHeight-150),(0,0,255),2)
                #cv2.putText(display_img, 'ENTER', (dspWidth-300,dspHeight-100), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255))
                #cv2.rectangle(display_img,(dspWidth-305,dspHeight-95),(dspWidth-75,dspHeight-150),(255,255,255),2)

                # display
                if (window_onece == True):
                    cv2.namedWindow('Display',  1)
                cv2.imshow('Display', display_img )
                if (window_onece == True):
                    #if (os.name == 'nt') \
                    #and ((dspWidth==1920 and dspHeight==1080) \
                    #  or (dspWidth==1280 and dspHeight== 720)):
                    #    cv2.moveWindow( 'Display', -18, -40)
                    #else:
                    cv2.moveWindow( 'Display',   0,   0)
                cv2.setMouseCallback('Display', DisplayMouseEvent)
                window_onece = False

                # KEYPRESS
                if (cv2.waitKey(10) >= 0):
                    qLogOutput('video_main:KEYPRESS!')
                    break

                # R-CLICK
                if (DisplayEvent == cv2.EVENT_RBUTTONDOWN):
                    DisplayEvent = None
                    qLogOutput('video_main:R-CLICK!')
                    #break

                # L-CLICK
                if (DisplayEvent == cv2.EVENT_LBUTTONUP):
                    DisplayEvent = None

                    # ENTER,CANCEL
                    if ((not MousePointX is None) and (not MousePointY is None)):
                        if (MousePointY <= dspHeight-150):
                                shutter_flag = True
                                qLogOutput('video_main:L-CLICK!')
                                #break
                        else:
                            if (MousePointX >= 0) and (MousePointX <= 350):
                                qLogOutput('video_main:CANCEL!')
                                break
                            elif (MousePointX >= dspWidth - 350) and (MousePointX <= dspWidth):
                                qLogOutput('video_main:ENTER!')
                                break
                            else:
                                shutter_flag = True
                                qLogOutput('video_main:L-CLICK!')
                                #break

                # SHUTTER
                if (shutter_flag == True):
                    shutter_flag = False
                    shutter_last = time.time()

                    # シャッター音
                    qGuide('_shutter', sync=False)

                    ## 白表示
                    white_img = np.zeros((dspHeight,dspWidth,3), np.uint8)
                    cv2.rectangle(white_img,(0,0),(dspWidth,dspHeight),(255,255,255),-1)
                    alpha_img= cv2.addWeighted(display_img, 0.5, white_img, 0.5, 0.0)
                    cv2.imshow('Display', alpha_img )
                    if cv2.waitKey(10) >= 0:
                        qLogOutput('video_main:KEYPRESS!')
                        break

                    # 保管
                    main_seq += 1
                    if (main_seq >= 10000):
                        main_seq = 1
                    seq4 = '{:04}'.format(main_seq)
                    seq2 = seq4[-2:]

                    now=datetime.datetime.now()
                    stamp=now.strftime('%Y%m%d.%H%M%S')
                    fileId = stamp + '.' + seq2

                    filename1=qPathRec   + fileId + '.photo.jpg'
                    filename2=qPathPhoto + fileId + '.photo.jpg'
                    qLogOutput(u'video_main: → ' + filename2)
                    try:
                        cv2.imwrite(filename1, inp1_img)
                        cv2.imwrite(filename2, inp1_img)
                    except:
                        pass

                    filename3=qPathRec   + fileId + '.screen.jpg'
                    filename4=qPathPhoto + fileId + '.screen.jpg'
                    try:
                        cv2.imwrite(filename3, display_img)
                        cv2.imwrite(filename4, display_img)
                    except:
                        pass

                    # ＣＶ
                    if (qApiCV != 'none') or (qApiOCR != 'none'):
                        main_cv(seq2, fileId, runMode, cam1Dev, filename1,)

        time.sleep(0.01)

    qLogOutput('')
    qLogOutput('video_main:terminate')

    try:
        cv2.destroyAllWindows
    except:
        pass

    try:
        inp1_s.put(    [None, None] )
        inp2_s.put(    [None, None] )
        compute_s.put( [None, None] )
        speech_s.put(  [None, None] )
        output_s.put(  [None, None] )
        time.sleep(3.00)
    except:
        pass

    try:
        inp1_proc.join()
        inp2_proc.join()
        compute_proc.join()
        speech_proc.join()
        output_proc.join()
    except:
        pass

    wrkText = u'画像制御機能を終了しました。'
    tts_speech(runMode, 'vision.99', wrkText, )

    qLogOutput('video_main:bye!')


