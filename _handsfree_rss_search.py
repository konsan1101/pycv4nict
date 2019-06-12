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

import urllib
import feedparser



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
        id  = 'rsssearch.' + '{:02}'.format(seq)
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
    qLogOutput('rss_main__:init')
    qLogOutput('rss_main__:exsample.py runMode, inpText, ')

    runMode = 'debug'
    inpText = u'姫路城'

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpText  = sys.argv[2]

    qLogOutput('rss_main__:runMode  =' + str(runMode  ))
    qLogOutput('rss_main__:inpText  =' + str(inpText  ))

    qLogOutput('rss_main__:start')

    if (True):

        try:

            s_quote = urllib.parse.quote(inpText)
            url = 'https://news.google.com/news/rss/search/section/q/' + s_quote + '/' + s_quote + '?ned=jp&hl=ja&gl=JP'

            rss = feedparser.parse(url)

            lang = 'ja,hoya,'
            speechs = []

            i = 0
            for entry in rss['entries']:
                i += 1
                #print("title:", entry.title)
                #print("published: ", entry.published)
                #print("link: ", entry.link)

                txt = entry.title
                txt = txt.replace(u'ニュース', u'ニュース.')

                #qLogOutput(' RSS Text  [' + str(txt)  + ']')
                #tts_speech(runMode, 'rsssearch.{:02}'.format(i), 'ja,hoya,' + txt, )
                speechs.append({'text':txt, 'wait':0, })

                if (i >= 5):
                    break

            txt = u'以上が、主なニュースです。'

            #qLogOutput(' RSS Text  [' + str(txt)  + ']')
            #tts_speech(runMode, 'rsssearch.99', 'ja,hoya,' + txt, )
            speechs.append({'text':txt, 'wait':0, })

            speech_run(runMode, speechs, lang, )
            speech_run(runMode, speechs, ''  , )

        except:
            pass



    qLogOutput('rss_main__:terminate')
    qLogOutput('rss_main__:bye!')



