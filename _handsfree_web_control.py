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

import requests as web
import bs4
import urllib.parse



qPathTTS   = 'temp/a3_5tts_txt/'
qCtrlWeb   = 'temp/temp_web_control.txt'

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



def web_open(runMode, inpText, url='', ):
    #url   = ''
    title = ''
    text  = ''

    if (url == ''):
        try:
            # キーワードを使って検索する
            list_keywd = [inpText]
            resp = web.get('https://www.google.co.jp/search?num=10&q=' + '　'.join(list_keywd))
            resp.raise_for_status()

            # 取得したHTMLをパースする
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
            link_elem01 = soup.select('.r > a')
            link_elem02 = soup.select('.s > .st')

            title = link_elem01[0].get_text()
            title = urllib.parse.unquote(title)

            text  = link_elem01[0].get_text()
            text  = urllib.parse.unquote(text)
            text  = text.replace('\n', '')

            url   = link_elem01[0].get('href')
            url   = url.replace('/url?q=', '')
            if (url.find('&sa=') >= 0):
                url = url[:url.find('&sa=')]
            url   = urllib.parse.unquote(url)
            url   = urllib.parse.unquote(url)

        except:
            pass

    if (url != ''):
        if (title != ''):
            qLogOutput(' Web Title [' + str(title) + ']')

        if (text != ''):
            qLogOutput(' Web Text  [' + str(text)  + ']')

            if (runMode=='debug' or runMode=='translator' or runMode=='learning'):
                wrkText = text + u'のホームページを表示します。'
                tts_speech(runMode, 'webcontrol.01', wrkText, )

        if (url[:4] != 'http'):
            url = 'https://google.co.jp' + url
        qLogOutput(' Web URL   [' + str(url)   + ']')

        if (os.name == 'nt'):
            #qKill('iexplore', )
            qKill('chrome', )
            #qKill('Safari', )
            #qKill('firefox', )
            #qKill('microsoftedge', )
        else:
            qKill('Goocle Chrome', )

        if (os.name == 'nt'):
            #browser = 'C:\\Program Files\\Internet Explorer\\iexplore.exe'
            browser = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            #browser = 'C:\\Program Files (x86)\\Safari\\Safari.exe'
            #browser = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
            #browser = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
            #browser = 'microsoft-edge:'
            bat = subprocess.Popen([browser, url, ], \
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            #bat.wait()
            #bat.terminate()
            #bat = None
        else:
            bat = subprocess.Popen(['open', '-a', 'Goocle Chrome', url, ], \
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            #bat.wait()
            #bat.terminate()
            #bat = None



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
    qLogOutput('web_main__:init')
    qLogOutput('web_main__:exsample.py runMode, inpFile, ')

    runMode = 'debug'
    inpFile = qCtrlWeb

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpFile  = sys.argv[2]

    qLogOutput('web_main__:runMode  =' + str(runMode  ))
    qLogOutput('web_main__:inpFile  =' + str(inpFile  ))

    tmpFile = inpFile[:-4] + '.tmp'

    qLogOutput('web_main__:start')



    wrkText = u'ブラウザー制御機能が起動しました。'
    tts_speech(runMode, 'webcontrol.00', wrkText, )

    #url='https://google.co.jp'
    url='https://www.pscp.tv/search?q=konsan1101'
    web_open(runMode=runMode, inpText='', url=url, )
    time.sleep(3.00)

    main_start = time.time()
    while (True):
        if (main_last is None):
            sec = int(time.time() - main_start)
            if (sec > 60):
                wrkText = u'何かＷｅｂ検索しませんか？'
                tts_speech(runMode, 'webcontrol.99', wrkText, )
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
                        #qLogOutput(u'★KONSAN : [' + str(inpText) + ']')
                        web_open(runMode=runMode, inpText=inpText, url='', )

        except:
            pass

        time.sleep(0.50)



    qLogOutput('web_main__:terminate')

    if (os.name == 'nt'):
        #qKill('iexplore', )
        qKill('chrome', )
        #qKill('Safari', )
        #qKill('firefox', )
        #qKill('microsoftedge', )
    else:
        qKill('Goocle Chrome', )

    wrkText = u'ブラウザー制御機能を終了しました。'
    tts_speech(runMode, 'webcontrol.99', wrkText, )

    qLogOutput('web_main__:bye!')


