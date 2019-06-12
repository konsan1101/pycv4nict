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

import random



qPathTTS   = 'temp/a3_5tts_txt/'
qPathPlay  = 'temp/a3_7play_voice/'

qPathWork  = 'temp/a3_9work/'
qBusyCtrl  = qPathWork + 'busy_speechctl.txt'
qBusyInput = qPathWork + 'busy_voice2wav.txt'
qBusySTT   = qPathWork + 'busy_sttcore.txt'
qBusyTTS   = qPathWork + 'busy_ttscore.txt'
qBusyPlay  = qPathWork + 'busy_playvoice.txt'



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



if (__name__ == '__main__'):
    qLogOutput('')
    qLogOutput('smart_spk_:init')
    qLogOutput('smart_spk_:exsample.py runMode, outText, outSmart,')

    runMode = 'debug'
    outText = u'今なんじ'
    outSmart= 'auto'

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        outText  = sys.argv[2]
    if (len(sys.argv) >= 4):
        outSmart = sys.argv[3]

    qLogOutput('smart_spk_:runMode  =' + str(runMode  ))
    qLogOutput('smart_spk_:outText  =' + str(outText  ))
    qLogOutput('smart_spk_:outSmart =' + str(outSmart ))

    qLogOutput('smart_spk_:start')

    if (True):

        smart = outSmart

        #smart = 'siri'
        #print('#############SIRI##############')

        if (smart == 'auto'):
            if (outText.find(u'現在地')>=0) \
            or (outText.find(u'ここ' )>=0) \
            or (outText.find(u'此処' )>=0):
                smart = 'siri'

        if (smart == 'auto'):
            i=random.randrange(1,4)
            if (i == 1):
                smart = 'siri'
            if (i == 2):
                smart = 'google'
            if (i == 3):
                smart = 'alexa'
            if (i == 4):
                smart = 'clova'

        speech_wait(idolsec=2, maxwait=15, )

        now=datetime.datetime.now()
        stamp=now.strftime('%Y%m%d-%H%M%S')

        if (smart == 'siri'):
            #txt = 'en,Hey, Siri'
            #tts_speech(runMode, id, txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sound_handsfree_ヘイSiri.mp3'
            print(mp3)
            wrkFile = qPathPlay + stamp + '.' + id + '.mp3'
            shutil.copy2(mp3, wrkFile)

            time.sleep(2.00)

            id  = 'smartspeaker.02'
            tts_speech(runMode, id, outText, idolsec=1, maxwait=0, )

        if (smart == 'google'):
            #txt = 'ja,ねぇグーグル'
            #tts_speech(runMode, 'smartspeaker.01', txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sound_handsfree_ねぇグーグル.mp3'
            print(mp3)
            wrkFile = qPathPlay + stamp + '.' + id + '.mp3'
            shutil.copy2(mp3, wrkFile)

            id  = 'smartspeaker.02'
            tts_speech(runMode, id, outText, idolsec=1, maxwait=0, )

        if (smart == 'alexa'):
            #txt = 'ja,アレクサ'
            #tts_speech(runMode, 'smartspeaker.01', txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sound_handsfree_アレクサ.mp3'
            print(mp3)
            wrkFile = qPathPlay + stamp + '.' + id + '.mp3'
            shutil.copy2(mp3, wrkFile)

            id  = 'smartspeaker.02'
            tts_speech(runMode, id, outText, idolsec=1, maxwait=0, )

        if (smart == 'clova'):
            #txt = 'ja,ねぇクローバ'
            #tts_speech(runMode, 'smartspeaker.01', txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sound_handsfree_ねぇクローバ.mp3'
            print(mp3)
            wrkFile = qPathPlay + stamp + '.' + id + '.mp3'
            shutil.copy2(mp3, wrkFile)

            id  = 'smartspeaker.02'
            tts_speech(runMode, id, outText, idolsec=1, maxwait=0, )



    qLogOutput('smart_spk_:terminate')
    qLogOutput('smart_spk_:bye!')


