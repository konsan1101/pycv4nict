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

# docomo 知識検索
import speech_api_docomo     as docomo_api
import speech_api_docomo_key as docomo_key



qPathTTS       = 'temp/a3_5tts_txt/'
qCtrlKnowledge = 'temp/temp_knowledge.txt'

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



def speech(docomoAPI, runMode, inpText, ):
    res, api = docomoAPI.knowledge(inpText=inpText, )
    if (res != '') and (res != '!'):
        if (res[:6] != u'ごめんなさい'):
            qLogOutput(u'★DOCOMO : [' + str(res) + ']')
            tts_speech(runMode, 'knowledge.01', 'ja,hoya,' + res, )
            tts_speech(runMode, 'knowledge.02', res, )
        else:
            txt = u'ごめんなさい。外部のＡＩに聞いてみます。'
            tts_speech(runMode, 'knowledge.00', txt, )

            time.sleep(5.00)

            speechtext = 'ja,hoya,' + inpText
            if (speechtext.find(u'ここ')>=0):
                smart = 'siri'
            else:
                smart = 'auto'
            smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                    #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            smtspk.wait()
            smtspk.terminate()
            smtspk = None



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



main_start = 0
main_last  = None
if (__name__ == '__main__'):
    qLogOutput('')
    qLogOutput('knowledge_:init')
    qLogOutput('knowledge_:exsample.py runMode, inpFile, ')

    runMode = 'debug'
    inpFile = qCtrlKnowledge
    inpText = ''

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpFile  = sys.argv[2]
    if (len(sys.argv) >= 4):
        inpText  = sys.argv[3]

    qLogOutput('knowledge_:runMode  =' + str(runMode  ))
    qLogOutput('knowledge_:inpFile  =' + str(inpFile  ))
    qLogOutput('knowledge_:inpText  =' + str(inpText  ))

    tmpFile = inpFile[:-4] + '.tmp'

    qLogOutput('knowledge_:start')

    docomoAPI = docomo_api.SpeechAPI()
    res_run = docomoAPI.authenticate('knowledge', docomo_key.getkey('knowledge'), )
    if (res_run):

        if (inpText != '') and (inpText != '!'):
            qLogOutput(u'★KONSAN : [' + str(inpText) + ']')
            speech(docomoAPI, runMode=runMode, inpText=inpText, )



        if (inpFile != ''):
            wrkText = u'DOCOMO知識データベース機能が起動しました。'
            tts_speech(runMode, 'knowledge.00', wrkText, )

        main_start = time.time()
        while (inpFile != ''):
            if (main_last is None):
                sec = int(time.time() - main_start)
                if (sec > 60):
                    wrkText = u'何かお調べしましょうか？'
                    tts_speech(runMode, 'knowledge.99', wrkText, )
                    main_last = time.time()

            try:
                if (os.path.exists(tmpFile)):
                    os.remove(tmpFile)

                if (os.path.exists(inpFile)):
                    os.rename(inpFile, tmpFile)

                if (os.path.exists(tmpFile)):
                    rt = codecs.open(tmpFile, 'r', 'shift_jis')
                    inpText = ''
                    for t in rt:
                        inpText = (inpText + ' ' + str(t)).strip()
                    rt.close
                    rt = None

                    if (inpText == '_close_'):
                        break

                    if (inpText != '_open_'):
                        if (inpText != '') and (inpText != '!'):
                            main_last = time.time()
                            qLogOutput(u'★KONSAN : [' + str(inpText) + ']')
                            speech(docomoAPI, runMode=runMode, inpText=inpText, )

            except:
                pass

            time.sleep(0.50)

        if (inpFile != ''):
            wrkText = u'DOCOMO知識データベース機能を終了しました。'
            tts_speech(runMode, 'knowledge.99', wrkText, )



    qLogOutput('knowledge_:terminate')
    qLogOutput('knowledge_:bye!')


