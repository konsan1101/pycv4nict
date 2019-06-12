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



qPathTTS   = 'temp/a3_5tts_txt/'
qCtrlBgm   = 'temp/temp_bgm_control.txt'

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
        


def bgm_open(runMode, inpText, ):
    global main_last

    procBgm = ''
    if (inpText == 'playlist 00'  ) or (inpText == 'playlist 0') \
    or (inpText == 'playlist zero') \
    or (inpText == 'bgm') or (inpText == 'garageband'):
        procBgm =  '_00_'

    if (inpText == 'playlist 01' ) or (inpText == 'playlist 1') \
    or (inpText == 'playlist etc') or (inpText == 'playlists etc'):
        procBgm =  '_01_'

    if (inpText == 'playlist 02') or (inpText == 'playlist 2') \
    or (inpText == 'babymetal'):
        procBgm =  '_02_'

    if (inpText == 'playlist 03') or (inpText == 'playlist 3') \
    or (inpText == 'perfume'):
        procBgm =  '_03_'

    if (inpText == 'playlist 04') or (inpText == 'playlist 4') \
    or (inpText == 'kyary pamyu pamyu'):
        procBgm =  '_04_'

    if (inpText == 'playlist 05') or (inpText == 'playlist 5') \
    or (inpText == 'one ok rock') or (inpText == 'one ok'):
        procBgm =  '_05_'

    if (inpText == 'playlist 06') or (inpText == 'playlist 6') \
    or (inpText == 'the end of the world') or (inpText == 'end of the world'):
        procBgm =  '_06_'

    if (inpText == 'playlist') or (inpText == 'playlist list') \
    or (inpText == 'list of playlists') or (inpText == 'bgm list'):
        wrkText = u'プレイリストゼロは、自作ＢＧＭです。'
        tts_speech(runMode, 'bgmcontrol.00', wrkText, )
        wrkText = u'プレイリスト１は、お気に入り音楽です。'
        tts_speech(runMode, 'bgmcontrol.01', wrkText, )
        wrkText = u'プレイリスト２は、「BABYMETAL」です。'
        tts_speech(runMode, 'bgmcontrol.02', wrkText, )
        wrkText = u'プレイリスト３は、「perfume」です。'
        tts_speech(runMode, 'bgmcontrol.03', wrkText, )
        wrkText = u'プレイリスト４は、「きゃりーぱみゅぱみゅ」です。'
        tts_speech(runMode, 'bgmcontrol.04', wrkText, )
        wrkText = u'プレイリスト５は、「ONE OK ROCK」です。'
        tts_speech(runMode, 'bgmcontrol.05', wrkText, )
        wrkText = u'プレイリスト６は、「SEKAI NO OWARI」です。'
        tts_speech(runMode, 'bgmcontrol.06', wrkText, )
        wrkText = u'プレイリストを再生しますか？'
        tts_speech(runMode, 'bgmcontrol.07', wrkText, )

    if (procBgm != ''):
        qKill('VLC', )

    if (procBgm != '_close_'):
        plist = ''
        pparm = ''
        if (os.name == 'nt'):
            if (procBgm == '_00_'):
                plist = u'C:\\Users\\Public\\_VLC_GB_プレイリスト.xspf'
                pparm = '--qt-start-minimized'
            if (procBgm == '_01_'):
                plist = u'C:\\Users\\Public\\_VLC_etc_プレイリスト.xspf'
            if (procBgm == '_02_'):
                plist = u'C:\\Users\\Public\\_VLC_BABYMETAL_プレイリスト.xspf'
            if (procBgm == '_03_'):
                plist = u'C:\\Users\\Public\\_VLC_Perfume_プレイリスト.xspf'
            if (procBgm == '_04_'):
                plist = u'C:\\Users\\Public\\_VLC_きゃりーぱみゅぱみゅ_プレイリスト.xspf'
            if (procBgm == '_05_'):
                plist = u'C:\\Users\\Public\\_VLC_ワンオク_プレイリスト.xspf'
            if (procBgm == '_06_'):
                plist = u'C:\\Users\\Public\\_VLC_セカオワ_プレイリスト.xspf'
            if (plist != ''):
                main_last = time.time()
                try:
                    if (pparm != ''):
                        bgm = subprocess.Popen(['VLC', pparm, plist, ], \
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    else:
                        bgm = subprocess.Popen(['VLC', plist, ], \
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    #bgm.wait()
                    #bgm.terminate()
                    #bgm = None
                except:
                    pass
        else:
            if (procBgm == '_00_'):
                plist = u'/users/kondou/Documents/_VLC_GB_プレイリスト.xspf'
                pparm = '--qt-start-minimized'
            if (procBgm == '_01_'):
                plist = u'/users/kondou/Documents/_VLC_etc_プレイリスト.xspf'
            if (procBgm == '_02_'):
                plist = u'/users/kondou/Documents/_VLC_BABYMETAL_プレイリスト.xspf'
            if (procBgm == '_03_'):
                plist = u'/users/kondou/Documents/_VLC_Perfume_プレイリスト.xspf'
            if (procBgm == '_04_'):
                plist = u'/users/kondou/Documents/_VLC_きゃりーぱみゅぱみゅ_プレイリスト.xspf'
            if (procBgm == '_05_'):
                plist = u'/users/kondou/Documents/_VLC_ワンオク_プレイリスト.xspf'
            if (procBgm == '_06_'):
                plist = u'/users/kondou/Documents/_VLC_セカオワ_プレイリスト.xspf'
            if (plist != ''):
                main_last = time.time()
                try:
                    if (pparm != ''):
                        #bgm = subprocess.Popen(['open', '-a', 'VLC', plist, pparm, ], \
                        bgm = subprocess.Popen(['open', '-a', 'VLC', plist, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    else:
                        bgm = subprocess.Popen(['open', '-a', 'VLC', plist, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    #bgm.wait()
                    #bgm.terminate()
                    #bgm = None
                except:
                    pass



def qKill(pName, ):
    if (os.name == 'nt'):
        try:
            kill = subprocess.Popen(['taskkill', '/im', pName + '.exe', '/f', ], \
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            kill.wait()
            kill.terminate()
            kill = None
        except:
            pass
    else:
        try:
            kill = subprocess.Popen(['pkill', '-9', '-f', pName, ], \
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            kill.wait()
            kill.terminate()
            kill = None
        except:
            pass



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
    qLogOutput('bgm_main__:init')
    qLogOutput('bgm_main__:exsample.py runMode, inpFile, ')

    runMode = 'debug'
    inpFile = qCtrlBgm

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpFile  = sys.argv[2]

    qLogOutput('bgm_main__:runMode  =' + str(runMode  ))
    qLogOutput('bgm_main__:inpFile  =' + str(inpFile  ))

    tmpFile = inpFile[:-4] + '.tmp'

    qLogOutput('bgm_main__:start')



    wrkText = u'ＢＧＭ制御機能が起動しました。'
    tts_speech(runMode, 'bgmcontrol.00', wrkText, )

    main_start = time.time()
    while (True):
            if (main_last is None):
                sec = int(time.time() - main_start)
                if (sec > 60):
                    wrkText = u'ＢＧＭを開始しましょうか？'
                    tts_speech(runMode, 'bgmcontrol.99', wrkText, )
                    main_last = time.time()

            #try:
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
                        #qLogOutput(u'★KONSAN : [' + str(inpText) + ']')
                        bgm_open(runMode=runMode, inpText=inpText, )

            #except:
            #pass

            time.sleep(0.50)



    qLogOutput('bgm_main__:terminate')

    qKill('VLC', )

    wrkText = u'ＢＧＭ制御機能を終了しました。'
    tts_speech(runMode, 'bgmcontrol.99', wrkText, )

    qLogOutput('bgm_main__:bye!')


