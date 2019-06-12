#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import queue
import threading
import subprocess
import datetime
import time
import codecs

# weather 天気予報
import speech_api_weather     as weather_api
import speech_api_weather_key as weather_key



qPathTTS   = 'temp/a3_5tts_txt/'

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

def speech_run(runMode, speechs, lang='ja,hoya,', idolsec=2, maxwait=15, ):

    speech_wait(idolsec,maxwait)

    seq = 0
    for speech in speechs:
        txt = lang + str(speech['text'])
        seq+= 1
        id  = 'weather.' + '{:02}'.format(seq)
        tts_speech(runMode, id, txt, 0, 0, )
        time.sleep(speech['wait'])



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
    qLogOutput('weather___:init')
    qLogOutput('weather___:exsample.py runMode, inpText, ')

    runMode = 'debug'
    inpText = u'三木市'

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpText  = sys.argv[2]

    qLogOutput('weather___:runMode  =' + str(runMode  ))
    qLogOutput('weather___:inpText  =' + str(inpText  ))

    qLogOutput('weather___:start')

    if (True):

        tenkiAPI = weather_api.WeatherAPI()

        city = inpText
        lang = 'ja,hoya,'

        api = 'openweathermap'
        key = weather_key.getkey(api)
        weather, temp_max, temp_min, humidity = \
            tenkiAPI.getWeather(api, key, city, )

        if (weather != ''):
            speechs = []
            speechs.append({'text':city + u'、今日の天気は、「' + weather + u'」です。', 'wait':0, })
            if (temp_max != ''):
                speechs.append({'text':u'最高気温は、' + temp_max + u'℃。', 'wait':0, })
            if (temp_min != ''):
                speechs.append({'text':u'最低気温は、' + temp_min + u'℃。', 'wait':0, })
            if (humidity != ''):
                speechs.append({'text':u'湿度は、' + humidity + u'%です。', 'wait':0, })
            speech_run(runMode, speechs, lang, )
            speech_run(runMode, speechs, ''  , )

        else:
            txt = u'ごめんなさい。外部のＡＩに聞いてみます。'
            tts_speech(runMode, 'weather.00', txt, )

            time.sleep(5.00)

            speechtext = 'ja,hoya,' + city + u'の天気？'
            smart = 'auto'
            smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                    #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            smtspk.wait()
            smtspk.terminate()
            smtspk = None



    qLogOutput('weather___:terminate')
    qLogOutput('weather___:bye!')


