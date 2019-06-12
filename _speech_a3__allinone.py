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

print(os.path.dirname(__file__))
print(os.path.basename(__file__))
print(sys.version_info)



qApiInp    = 'free'
qApiTrn    = 'free'
qApiOut    = 'free'
if (qOS == 'windows'):
    qApiOut = 'winos'
if (qOS == 'darwin'):
    qApiOut = 'macos'
qLangInp   = 'ja'
qLangTrn   = 'en'
qLangTxt   = qLangInp
qLangOut   = qLangTrn[:2]

qPathCtrl  = 'temp/a3_0control/'
qPathInp   = 'temp/a3_1voice/'
qPathWav   = 'temp/a3_2stt_wav/'
qPathSTT   = 'temp/a3_3stt_txt/'
qPathTTS   = 'temp/a3_5tts_txt/'
qPathTRA   = 'temp/a3_6tra_txt/'
qPathPlay  = 'temp/a3_7play_voice/'
qPathRec   = 'temp/a3_8recorder/'
qPathWork  = 'temp/a3_9work/'

qBusyCtrl  = qPathWork + 'busy_speechctl.txt'
qBusyInput = qPathWork + 'busy_voice2wav.txt'
qBusySTT   = qPathWork + 'busy_sttcore.txt'
qBusyTTS   = qPathWork + 'busy_ttscore.txt'
qBusyPlay  = qPathWork + 'busy_playvoice.txt'

qCtrlBgm       = 'temp/temp_bgm_control.txt'
qCtrlWeb       = 'temp/temp_web_control.txt'
qCtrlChatting  = 'temp/temp_chatting.txt'
qCtrlKnowledge = 'temp/temp_knowledge.txt'
qCtrlVision    = 'temp/temp_vision.txt'
qCtrlRecognize = 'temp/temp_recognize.txt'
qCtrlTranslate = 'temp/temp_translate.txt'



def qBusySet(file, sw=True):
    if (sw == True):
        chktime = time.time()
        while (not os.path.exists(file)) and ((time.time() - chktime) < 1):
            try:
                w = open(file, 'w')
                w.write('BUSY')
                w.close()
                w = None
            except:
                w = None
            time.sleep(0.10)
    else:
        chktime = time.time()
        while (os.path.exists(file)) and ((time.time() - chktime) < 1):
            try:
                os.remove(file)
            except:
                pass
            time.sleep(0.10)

def qBusyCheck(file, sec):
    chktime = time.time()
    while (os.path.exists(file)) and ((time.time() - chktime) < sec):
        time.sleep(0.10)
    if (os.path.exists(file)):
        return 'busy'
    else:
        return 'none'

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



def control_speech(seq, fileId, runMode, micDev, useApiTrn, useApiOut, inpLang, outLang, speechtext, sync=True):
    global qPathPlay
    global qPathWork
    global qBusyPlay

    xrunMode = runMode
    xApiInp  = qApiInp
    xApiTrn  = useApiTrn
    xApiOut  = useApiOut
    xLangInp = inpLang
    xLangTrn = outLang
    xLangTxt = inpLang
    xLangOut = outLang

    #while qBusyCheck(qBusyPlay , 0) == 'busy':
    #    qLogOutput('wait')
    #    time.sleep(1)

    if (True):
        now=datetime.datetime.now()
        stamp=now.strftime('%Y%m%d-%H%M%S')
        wrkText = qPathWork + stamp + '.' + seq + '.control.txt'
        wrkOut  = qPathPlay + stamp + '.' + seq + '.control.mp3'

        try:
            w = codecs.open(wrkText, 'w', 'utf-8')
            w.write(speechtext)
            w.close()
            w = None
        except:
            w = None

    if (True):
        inpInput = ''
        inpOutput= ''
        trnInput = ''
        trnOutput= ''
        txtInput = wrkText
        txtOutput= wrkOut
        outInput = ''
        outOutput= ''
        inpPlay  = 'off'
        txtPlay  = 'off'
        outPlay  = 'off'

    if (True):
        api = subprocess.Popen(['python', '_speech_a3_all_api.py', \
              xrunMode, micDev, xApiInp, xApiTrn, xApiOut, xLangInp, xLangTrn, xLangTxt, xLangOut, \
              str(seq), fileId, inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput, \
              inpPlay, txtPlay, outPlay, ], \
              )

        if (sync == True):
            api.wait()
            api.terminate()
            api = None



locked_ai         = False
bgm_control       = None
web_control       = None
chatting_control  = None
knowledge_control = None
vision_control    = None
def control_sub(seq, fileId, runMode, micDev, cmdtxt, cmdLang, ):
    global qOS
    global qApiInp
    global qApiTrn
    global qApiOut
    global qLangInp
    global qLangTrn
    global qLangTxt
    global qLangOut

    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    global qBusyCtrl
    global qBusyInput
    global qBusySTT
    global qBusyTTS
    global qBusyPlay

    global qCtrlBgm
    global qCtrlWeb
    global qCtrlChatting
    global qCtrlKnowledge
    global qCtrlVision

    global locked_ai
    global bgm_control
    global web_control
    global chatting_control
    global knowledge_control
    global vision_control

    cmdtxt=cmdtxt.lower()

    procText      = cmdtxt
    cmdBgm        = ''
    cmdWeb        = ''
    cmdChatting   = ''
    cmdKnowledge  = ''
    cmdVision     = ''

    if (runMode=='speech') or (runMode=='number'):
        procText = ''

    if (runMode=='translator') or (runMode=='learning'):
        procText = ''

    if (runMode=='knowledge'):
        procText = ''

    #if (runMode=='debug') or (runMode=='handsfree'):
    if (procText != ''):

        if (cmdLang == 'ja'):
            if (procText == 'default' or procText == 'by default') \
            or (procText == 'special') \
            or (procText == 'google') \
            or (procText == 'ibm') or (procText == 'watson') \
            or (procText == 'microsoft' or procText == 'google' or procText == 'azur') \
            or (procText == 'nict') or (procText == 'n i c t') \
            or (procText == 'contest') or (procText == 'contests') \
            or (procText == 'contesting possession') \
            or (procText == 'presentation') \
            or (procText == 'docomo') \
            or (procText == 'winos') or (procText == 'windows') \
            or (procText == 'macos') or (procText == 'osx') \
            or (procText == 'audio stop') or (procText == 'voice stop') \
            or (procText == 'ai lock') or (procText == 'api lock') \
            or (procText == 'artificial intelligence fixation') \
            or (procText == 'ai list') or (procText == 'api list') \
            or (procText == 'ai test') or (procText == 'api test'):
                procText = ''

            if (procText == u'システム終了' or procText == u'バルス'):
                cmdBgm       = '_close_'
                cmdWeb       = '_close_'
                cmdChatting  = '_close_'
                cmdKnowledge = '_close_'
                cmdVision    = '_close_'

        if (cmdLang == 'en'):
            if ((procText.find('play'     )>=0) and (procText.find('list' )>=0)) \
            or ((procText.find('play'     )>=0) and (procText.find('start')>=0)) \
            or ((procText.find('playlist' )>=0) and (procText.find('start')>=0)) \
            or ((procText.find('play list')>=0) and (procText.find('start')>=0)) \
            or ((procText.find('bgm')      >=0) and (procText.find('start')>=0)) \
            or (procText == 'bgm') \
            or (procText == 'garageband') \
            or (procText == 'babymetal') \
            or (procText == 'perfume') \
            or (procText == 'kyary pamyu pamyu') \
            or (procText == 'one ok rock' or procText == 'one ok') \
            or (procText == 'the end of the world' or procText == 'end of the world'):
                cmdBgm = '_open_'

            if ((procText.find('playlist') >=0) and (procText.find('end'  )>=0)) \
            or ((procText.find('playlist') >=0) and (procText.find('stop' )>=0)) \
            or ((procText.find('playlist') >=0) and (procText.find('close')>=0)) \
            or ((procText.find('playlist') >=0) and (procText.find('exit' )>=0)) \
            or ((procText.find('play list')>=0) and (procText.find('end'  )>=0)) \
            or ((procText.find('play list')>=0) and (procText.find('stop' )>=0)) \
            or ((procText.find('play list')>=0) and (procText.find('close')>=0)) \
            or ((procText.find('play list')>=0) and (procText.find('exit' )>=0)) \
            or ((procText.find('bgm')      >=0) and (procText.find('end'  )>=0)) \
            or ((procText.find('bgm')      >=0) and (procText.find('stop' )>=0)) \
            or ((procText.find('bgm')      >=0) and (procText.find('close')>=0)) \
            or ((procText.find('bgm')      >=0) and (procText.find('exit' )>=0)):
                cmdBgm = '_close_'

            if ((procText.find('browser')>=0) and (procText.find('start')>=0)) \
            or (procText == 'browser') \
            or (procText == 'web browser') \
            or (procText == 'periscope'):
                cmdWeb = '_open_'

            if ((procText.find('browser')>=0) and (procText.find('end'  )>=0)) \
            or ((procText.find('browser')>=0) and (procText.find('stop' )>=0)) \
            or ((procText.find('browser')>=0) and (procText.find('close')>=0)) \
            or ((procText.find('browser')>=0) and (procText.find('exit' )>=0)):
                cmdWeb = '_close_'

            if ((procText.find('chat')>=0) and (procText.find('start')>=0)) \
            or (procText == 'chat'):
                cmdChatting = '_open_'

            if ((procText.find('chat')>=0) and (procText.find('end'  )>=0)) \
            or ((procText.find('chat')>=0) and (procText.find('stop' )>=0)) \
            or ((procText.find('chat')>=0) and (procText.find('close')>=0)) \
            or ((procText.find('chat')>=0) and (procText.find('exit' )>=0)):
                cmdChatting = '_close_'

            if ((procText.find('knowledge')>=0) and (procText.find('start')>=0)) \
            or (procText == 'knowledge') \
            or (procText == 'knowledge database'):
                cmdKnowledge = '_open_'

            if ((procText.find('knowledge')>=0) and (procText.find('end'  )>=0)) \
            or ((procText.find('knowledge')>=0) and (procText.find('stop' )>=0)) \
            or ((procText.find('knowledge')>=0) and (procText.find('close')>=0)) \
            or ((procText.find('knowledge')>=0) and (procText.find('exit' )>=0)):
                cmdKnowledge = '_close_'

            if ((procText.find('image') >=0) and (procText.find('start')>=0)) \
            or ((procText.find('vision')>=0) and (procText.find('start')>=0)) \
            or (procText == 'image') \
            or (procText == 'image control') \
            or (procText == 'vision') \
            or (procText == 'vision control'):
                cmdVision = '_open_'

            if ((procText.find('shutter')>=0) or (procText.find('photo')>=0)):
                cmdVision = '_shutter_'

            if ((procText == 'zoom') or (procText == 'zoom in')):
                cmdVision = '_zoom_in_'

            if ((procText == 'zoom out') or (procText == 'zoom off')):
                cmdVision = '_zoom_out_'

            if ((procText.find('image') >=0) and (procText.find('end'  )>=0)) \
            or ((procText.find('image') >=0) and (procText.find('stop' )>=0)) \
            or ((procText.find('image') >=0) and (procText.find('close')>=0)) \
            or ((procText.find('image') >=0) and (procText.find('exit' )>=0)) \
            or ((procText.find('vision')>=0) and (procText.find('end'  )>=0)) \
            or ((procText.find('vision')>=0) and (procText.find('stop' )>=0)) \
            or ((procText.find('vision')>=0) and (procText.find('close')>=0)) \
            or ((procText.find('vision')>=0) and (procText.find('exit' )>=0)):
                cmdVision = '_close_'

            if (procText == 'reset'):
                cmdBgm       = '_close_'
                cmdWeb       = '_close_'
                cmdChatting  = '_close_'
                cmdKnowledge = '_close_'
                cmdVision    = '_close_'



        if (cmdBgm       != '') \
        or (cmdWeb       != '') \
        or (cmdChatting  != '') \
        or (cmdKnowledge != '') \
        or (cmdVision    != '') \
        or (procText == 'default' or procText == 'by default') \
        or (procText == 'special') \
        or (procText == 'google') \
        or (procText == 'ibm') or (procText == 'watson') \
        or (procText == 'microsoft' or procText == 'google' or procText == 'azur') \
        or (procText == 'nict') or (procText == 'n i c t') \
        or (procText == 'contest') or (procText == 'contests') \
        or (procText == 'contesting possession') \
        or (procText == 'presentation') \
        or (procText == 'docomo') \
        or (procText == 'winos') or (procText == 'windows') \
        or (procText == 'macos') or (procText == 'osx') \
        or (procText == 'audio stop') or (procText == 'voice stop') \
        or (procText == 'ai lock') or (procText == 'api lock') \
        or (procText == 'artificial intelligence fixation') \
        or (procText == 'ai list') or (procText == 'api list') \
        or (procText == 'ai test') or (procText == 'api test') \
        or (procText == u'言語は何ですか') or (procText == u'何語ですか') \
        or (procText == u'日本語'         and qLangOut != 'ja') \
        or (procText == u'英語'           and qLangOut != 'en') \
        or (procText == u'アラビア語'     and qLangOut != 'ar') \
        or (procText == u'スペイン語'     and qLangOut != 'es') \
        or (procText == u'ドイツ語'       and qLangOut != 'de') \
        or (procText == u'フランス語'     and qLangOut != 'fr') \
        or (procText == u'イタリア語'     and qLangOut != 'it') \
        or (procText == u'ポルトガル語'   and qLangOut != 'pt') \
        or (procText == u'ロシア語'       and qLangOut != 'ru') \
        or (procText == u'トルコ語'       and qLangOut != 'tr') \
        or (procText == u'ウクライナ語'   and qLangOut != 'uk') \
        or (procText == u'インドネシア語' and qLangOut != 'id') \
        or (procText == u'ミャンマー語'   and qLangOut != 'my') \
        or (procText == u'タイ語'         and qLangOut != 'th') \
        or (procText == u'ベトナム語'     and qLangOut != 'vi') \
        or (procText == u'中国語'         and qLangOut != 'zh') \
        or (procText == u'韓国語'         and qLangOut != 'ko') \
        or (procText == u'デモ紹介') or (procText == u'デモンストレーション') \
        or (procText == u'自己紹介') or (procText == u'自己診断') \
        or (procText == u'翻訳紹介') or (procText == u'翻訳診断') \
        or (procText == u'連携紹介') or (procText == u'連携診断') \
        or (procText == u'今何時') or (procText == u'今何時？') \
        or (procText == u'現在地') or (procText == u'ここはどこ') \
        or (procText == u'個人の予定') or (procText == u'個人のスケジュール') \
        or (procText == u'会社の予定') or (procText == u'会社のスケジュール') \
        or (procText == u'今日の予定') or (procText == u'今日のスケジュール') \
        or (procText[-4:] == u'電話して' or procText[-5:] == u'ラインして') \
        or (procText[-2:] == u'経路' or procText[-2:] == u'道順') \
        or (procText[-2:] == u'時間' or procText[-2:] == u'時刻') \
        or (procText[-3:] == u'調べて' or procText[-3:] == u'教えて') \
        or (procText[-4:] == u'ニュース') \
        or (procText[-3:] == u'の天気'):

            qLogOutput(procText)

            if (not bgm_control is None):
                 if (cmdBgm != ''):
                    try:
                        w = codecs.open(qCtrlBgm, 'w', 'shift_jis')
                        if (cmdBgm != '_close_'):
                            w.write(procText)
                        else:
                            w.write(cmdBgm)
                        w.close()
                        w = None
                    except:
                        w = None

            if (not web_control is None):
                if (cmdWeb != ''):
                    try:
                        print ('web control' + cmdWeb)
                        w = codecs.open(qCtrlWeb, 'w', 'shift_jis')
                        w.write(cmdWeb)
                        w.close()
                        w = None
                    except:
                        w = None

            if (not chatting_control is None):
                if (cmdChatting != ''):
                    try:
                        w = codecs.open(qCtrlChatting, 'w', 'shift_jis')
                        w.write(cmdChatting)
                        w.close()
                        w = None
                    except:
                        w = None

            if (not knowledge_control is None):
                if (cmdKnowledge != ''):
                    try:
                        w = codecs.open(qCtrlKnowledge, 'w', 'shift_jis')
                        w.write(cmdKnowledge)
                        w.close()
                        w = None
                    except:
                        w = None

            if (not vision_control is None):
                if (cmdVision != ''):
                    try:
                        w = codecs.open(qCtrlVision, 'w', 'shift_jis')
                        w.write(cmdVision)
                        w.close()
                        w = None
                    except:
                        w = None

        else:

            if (not web_control is None):
                if (cmdLang == 'ja'):
                    try:
                        print ('web control' + procText)
                        w = codecs.open(qCtrlWeb, 'w', 'shift_jis')
                        w.write(procText)
                        w.close()
                        w = None
                    except:
                        w = None

            if (not chatting_control is None):
                if (cmdLang == 'ja'):
                    try:
                        w = codecs.open(qCtrlChatting, 'w', 'shift_jis')
                        w.write(procText)
                        w.close()
                        w = None
                    except:
                        w = None

            if (not knowledge_control is None):
                if (cmdLang == 'ja'):
                    try:
                        w = codecs.open(qCtrlKnowledge, 'w', 'shift_jis')
                        w.write(procText)
                        w.close()
                        w = None
                    except:
                        w = None

            procText=''



    if (procText != ''):

        #time.sleep(2.00)

        if (qBusyCheck(qBusyCtrl  , 0) != 'busy'):
            qBusySet(qBusyCtrl,  True)
            #qBusyCheck(qBusyCtrl , 3)
            #qBusyCheck(qBusySTT  , 3)
            #qBusyCheck(qBusyTTS  , 3)
            qBusyCheck(qBusyPlay , 3)
            if (micType == 'bluetooth') or (micGuide == 'on' or micGuide == 'sound'):
                qBusyCheck(qBusyInput , 3)



    if (cmdBgm == '_open_'):
        if (bgm_control is None):
            bgm_control = subprocess.Popen(['python', '_handsfree_bgm_control.py', runMode, qCtrlBgm, ], )
                          #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            #bgm_control.wait()
            #bgm_control.terminate()
            #bgm_control = None

    if (cmdBgm == '_close_'):
        if (not bgm_control is None):
            bgm_control.wait()
            bgm_control.terminate()
            bgm_control = None



    if (cmdWeb == '_open_'):
        if (web_control is None):
            web_control = subprocess.Popen(['python', '_handsfree_web_control.py', runMode, qCtrlWeb, ], )
                          #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            #web_control.wait()
            #web_control.terminate()
            #web_control = None

    if (cmdWeb == '_close_'):
        if (not web_control is None):
            web_control.wait()
            web_control.terminate()
            web_control = None



    if (cmdChatting == '_open_'):
        if (chatting_control is None):
            chatting_control = subprocess.Popen(['python', '_handsfree_chatting_control.py', runMode, qCtrlChatting, ], )
                               #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            #chatting_control.wait()
            #chatting_control.terminate()
            #chatting_control = None

    if (cmdChatting == '_close_'):
        if (not chatting_control is None):
            chatting_control.wait()
            chatting_control.terminate()
            chatting_control = None



    if (cmdKnowledge == '_open_'):
        if (knowledge_control is None):
            knowledge_control = subprocess.Popen(['python', '_handsfree_knowledge_control.py', runMode, qCtrlKnowledge, '', ], )
                                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            #knowledge_control.wait()
            #knowledge_control.terminate()
            #knowledge_control = None

    if (cmdKnowledge == '_close_'):
        if (not knowledge_control is None):
            knowledge_control.wait()
            knowledge_control.terminate()
            knowledge_control = None



    if (cmdVision == '_open_'):
        if (vision_control is None):
            vision_control = subprocess.Popen(['python', '_vision_v3__capture.py', runMode, ], )
                             #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            #vision_control.wait()
            #vision_control.terminate()
            #vision_control = None

    if (cmdVision == '_close_'):
        if (not vision_control is None):
            vision_control.wait()
            vision_control.terminate()
            vision_control = None



    if (procText == u'言語は何ですか') or (procText == u'何語ですか'):
        speechtext  = u'この翻訳機能は、'
        speechtext += u'日本語、英語、アラビア語、スペイン語、ドイツ語、フランス語、'
        speechtext += u'イタリア語、ポルトガル語、ロシア語、トルコ語、ウクライナ語、'
        speechtext += u'インドネシア語、ミャンマー語、タイ語、ベトナム語、'
        speechtext += u'中国語ならびに韓国語'
        speechtext += u'に翻訳できます。あなたは何語を話しますか？'
        speechtext += u'「konsan」にはシンプル英文メッセージでお願いします。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, 'en', speechtext, )

    if (procText == u'日本語'         and qLangOut != 'ja'):
        qLangOut = 'ja'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'英語'           and qLangOut != 'en'):
        qLangOut = 'en'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'アラビア語'     and qLangOut != 'ar'):
        qLangOut = 'ar'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'スペイン語'     and qLangOut != 'es'):
        qLangOut = 'es'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'ドイツ語'       and qLangOut != 'de'):
        qLangOut = 'de'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'フランス語'     and qLangOut != 'fr'):
        qLangOut = 'fr'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'イタリア語'     and qLangOut != 'it'):
        qLangOut = 'it'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'ポルトガル語'   and qLangOut != 'pt'):
        qLangOut = 'pt'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'ロシア語'       and qLangOut != 'ru'):
        qLangOut = 'ru'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'トルコ語'       and qLangOut != 'tr'):
        qLangOut = 'tr'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'ウクライナ語'   and qLangOut != 'uk'):
        qLangOut = 'uk'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'インドネシア語' and qLangOut != 'id'):
        qLangOut = 'id'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'ミャンマー語'   and qLangOut != 'my'):
        qLangOut = 'my'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'タイ語'         and qLangOut != 'th'):
        qLangOut = 'th'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'ベトナム語'     and qLangOut != 'vi'):
        qLangOut = 'vi'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'中国語'         and qLangOut != 'zh'):
        qLangOut = 'zh'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == u'韓国語'         and qLangOut != 'ko'):
        qLangOut = 'ko'
        qLangTrn = qLangOut
        speechtext = u'音声言語を、' + cmdtxt + u'に切り替えました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if (procText == u'デモ紹介') or (procText == u'デモンストレーション'):
                selfcheck = subprocess.Popen(['python', '_handsfree_self_check.py', runMode, u'demo', ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                #selfcheck.wait()
                #selfcheck.terminate()
                #selfcheck = None

    if (procText == u'自己紹介') or (procText == u'自己診断'):
                selfcheck = subprocess.Popen(['python', '_handsfree_self_check.py', runMode, 'all', ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                #selfcheck.wait()
                #selfcheck.terminate()
                #selfcheck = None

    if (procText == u'翻訳紹介') or (procText == u'翻訳診断'):
                selfcheck = subprocess.Popen(['python', '_handsfree_self_check.py', runMode, u'翻訳', ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                #selfcheck.wait()
                #selfcheck.terminate()
                #selfcheck = None

    if (procText == u'ハンズフリー紹介') or (procText == u'ハンズフリー診断'):
                selfcheck = subprocess.Popen(['python', '_handsfree_self_check.py', runMode, u'ハンズフリー', ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                #selfcheck.wait()
                #selfcheck.terminate()
                #selfcheck = None

    if (procText == u'連携紹介') or (procText == u'連携診断'):
                selfcheck = subprocess.Popen(['python', '_handsfree_self_check.py', runMode, u'連携', ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                #selfcheck.wait()
                #selfcheck.terminate()
                #selfcheck = None

    if (procText == u'今何時') or (procText == u'今何時？'):
        #now2=datetime.datetime.now()
        #speechtext  = u'日本の現在の時刻は、'
        #speechtext += now2.strftime('%H') + u'時'
        #speechtext += now2.strftime('%M') + u'分です'
        #control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

        speechtext  = u'ja,hoya,今なんじ？'
        if   (qApiOut == 'google'):
                smart = 'alexa'
                smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                        #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                smtspk.wait()
                smtspk.terminate()
                smtspk = None
        elif (qApiOut == 'free' or qApiOut == 'winos'):
                smart = 'clova'
                smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                        #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                smtspk.wait()
                smtspk.terminate()
                smtspk = None
        else:
                smart = 'google'
                smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                        #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                smtspk.wait()
                smtspk.terminate()
                smtspk = None

    if (procText == u'現在地') or (procText == u'ここはどこ'):
                speechtext = 'ja,hoya,' + procText + '？'
                smart = 'siri'
                smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                        #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                smtspk.wait()
                smtspk.terminate()
                smtspk = None

    if (procText == u'会社の予定') or (procText == u'会社のスケジュール') \
    or (procText == u'今日の予定') or (procText == u'今日のスケジュール'):
                speechtext = u'ja,hoya,今日の予定教えて？'
                smart = 'alexa'
                smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                        #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                smtspk.wait()
                smtspk.terminate()
                smtspk = None

    if (procText == u'今日の予定') or (procText == u'今日のスケジュール'):
                time.sleep(10.00)

    if (procText == u'個人の予定') or (procText == u'個人のスケジュール') \
    or (procText == u'今日の予定') or (procText == u'今日のスケジュール'):
                speechtext = u'ja,hoya,今日の予定教えて？'
                smart = 'google'
                smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                        #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                smtspk.wait()
                smtspk.terminate()
                smtspk = None

    if (procText[-4:] == u'電話して' or procText[-5:] == u'ラインして'):
                speechtext = 'ja,hoya,' + procText + '。'
                smart = 'clova'
                smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                        #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                smtspk.wait()
                smtspk.terminate()
                smtspk = None

    if (procText[-2:] == u'経路' or procText[-2:] == u'道順'):
                speechtext = 'ja,hoya,' + procText + '。'
                smart = 'siri'
                smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                        #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                smtspk.wait()
                smtspk.terminate()
                smtspk = None

    if (procText[-2:] == u'時間' or procText[-2:] == u'時刻'):
                speechtext = 'ja,hoya,' + procText + '。'
                smart = 'auto'
                smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                        #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                smtspk.wait()
                smtspk.terminate()
                smtspk = None

    if (procText[-3:] == u'調べて' or procText[-3:] == u'教えて'):
                speechtext = procText + '？'
                knowledge_onece = subprocess.Popen(['python', '_handsfree_knowledge_control.py', runMode, '', speechtext, ], )
                                  #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                knowledge_onece.wait()
                knowledge_onece.terminate()
                knowledge_onece = None

    if (procText[-4:] == u'ニュース'):
                rss = subprocess.Popen(['python', '_handsfree_rss_search.py', runMode, procText, ], )
                      #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                #rss.wait()
                #rss.terminate()
                #rss = None

    if (procText[-3:] == u'の天気'):
                weather = subprocess.Popen(['python', '_handsfree_weather_search.py', runMode, procText[:-3], ], )
                          #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                #weather.wait()
                #weather.terminate()
                #weather = None



    if (procText == 'ai lock') or (procText == 'api lock') \
    or (procText == 'artificial intelligence fixation'):
        locked_ai = True
        speechtext = u'ja,hoya,クラウドAIの切り替えをロックします。'
        control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'クラウドAIの切り替えをロックしました。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'再起動以外解除できません。'
        control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (procText == 'ai list') or (procText == 'api list'):
        speechtext = u'ja,hoya,利用可能なAIをお知らせします。'
        control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'現在利用可能なクラウドAIは、次の通りです。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'グーグルクラウドプラットホームのAI。'
        control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'ＩＢＭのクラウドAI「WATSON」。'
        control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'マイクロソフトのクラウドAI「azure」。'
        control_speech('04', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'国立法人の情報通信研究機構「ＮＩＣＴ」のクラウドAI。'
        control_speech('05', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'携帯電話会社「ドコモ」の音声認識機能、雑談会話機能、知識データベース検索機能。'
        control_speech('06', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'「ＨＯＹＡ」の音声合成機能。'
        control_speech('07', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'また、場合により外部スマートスピーカー、ｉＰｈｏｎｅとも連携できます。'
        control_speech('08', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'クラウドAIを切り替えしますか？'
        control_speech('99', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if (procText == 'default' or procText == 'by default') and (locked_ai == False):
        if  (qApiInp == 'free') and (qApiTrn == 'free') \
        and (qApiOut == 'free' or qApiOut == 'winos' or qApiOut == 'macos') \
        and (qLangOut == 'en') and (qLangTrn[:2] == qLangOut):
            speechtext = u'ja,hoya,既にデフォルト設定で処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,デフォルト設定に移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qLangTrn = 'en'
            qLangOut = qLangTrn[:2]

            qApiInp = 'free'
            qApiTrn = 'free'
            qApiOut = 'free'
            if (qOS == 'windows'):
                qApiOut = 'winos'
            if (qOS == 'darwin'):
                qApiOut = 'macos'

            useApi = qApiInp
            speechtext = u'音声認識機能と翻訳機能は、グーグルクラウドプラットホームのAIで処理します。'
            control_speech('01', fileId, runMode, micDev, useApi, useApi, qLangInp, qLangOut, speechtext, )
            if   (qApiOut == 'winos'):
                speechtext = u'音声合成機能は、WINDOWSのOSで処理します。'
            elif (qApiOut == 'macos'):
                speechtext = u'音声合成機能は、MacのOSで処理します。'
            else:
                speechtext = u'音声合成機能も、グーグルクラウドプラットホームのAIで処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'よろしくお願いします。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, 'free', qLangInp, qLangOut, speechtext, False)
            control_speech('04', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, False)



    if (procText == 'special') and (locked_ai == False):
        if  (qApiInp == 'google') and (qApiTrn == 'azure') and (qApiOut == 'watson') \
        and (qLangOut == 'en') and (qLangTrn[:2] == qLangOut):
            speechtext = u'ja,hoya,既にスペシャル設定で処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,スペシャル設定に移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qLangTrn = 'en'
            qLangOut = qLangTrn[:2]

            qApiInp = 'google'
            qApiTrn = 'azure'
            qApiOut = 'watson'

            useApi = qApiInp
            speechtext = u'こんにちは。私はグーグルクラウドプラットホームのAIです。'
            control_speech('01', fileId, runMode, micDev, useApi, useApi, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声認識機能は、グーグルクラウドプラットホームのAIが処理します。'
            control_speech('02', fileId, runMode, micDev, useApi, useApi, qLangInp, qLangOut, speechtext, )

            useApi = qApiTrn
            speechtext = u'こんにちは。私はマイクロソフトのクラウドAI「azure」です。'
            control_speech('03', fileId, runMode, micDev, useApi, useApi, qLangInp, qLangOut, speechtext, )
            speechtext = u'機械翻訳機能は、マイクロソフトのクラウドAI「azure」が処理します。'
            control_speech('04', fileId, runMode, micDev, useApi, useApi, qLangInp, qLangOut, speechtext, )

            useApi = qApiOut
            speechtext = u'こんにちは。私はＩＢＭのクラウドAI「WATSON」です。'
            control_speech('05', fileId, runMode, micDev, useApi, useApi, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声合成機能は、ＩＢＭのクラウドAI「WATSON」が処理します。'
            control_speech('06', fileId, runMode, micDev, useApi, useApi, qLangInp, qLangOut, speechtext, )

            speechtext = u'よろしくお願いします。'
            control_speech('07', fileId, runMode, micDev, qApiInp, qApiInp,   qLangInp, qLangOut, speechtext, False)
            control_speech('08', fileId, runMode, micDev, qApiTrn, qApiTrn,  qLangInp, qLangOut, speechtext, False)
            control_speech('09', fileId, runMode, micDev, qApiOut, qApiOut, qLangInp, qLangOut, speechtext, False)



    if (procText == 'google') and (locked_ai == False):
        if  (qApiInp == 'google') and (qApiTrn == qApiInp) and (qApiOut == qApiInp) \
        and (qLangOut == 'en') and (qLangTrn[:2] == qLangOut):
            speechtext = u'ja,hoya,既にグーグルクラウドプラットホームのAIで処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,グーグルクラウドプラットホームのAIに移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qLangTrn = 'en'
            qLangOut = qLangTrn[:2]

            qApiInp = 'google'
            qApiTrn = 'google'
            qApiOut = 'google'
            speechtext = u'こんにちは。私はグーグルクラウドプラットホームのAIです。'
            control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声認識機能、機械翻訳機能、音声合成機能は、グーグルクラウドプラットホームのAIが処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'よろしくお願いします。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if (procText == 'ibm' or procText == 'watson') and (locked_ai == False):
        if  (qApiInp == 'watson') and (qApiTrn == qApiInp) and (qApiOut == qApiInp) \
        and (qLangOut == 'en') and (qLangTrn[:2] == qLangOut):
            speechtext = u'ja,hoya,既にＩＢＭのクラウドAI「WATSON」で処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,ＩＢＭのクラウドAI「WATSON」に移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qLangTrn = 'en'
            qLangOut = qLangTrn[:2]

            qApiInp = 'watson'
            qApiTrn = 'watson'
            qApiOut = 'watson'
            speechtext = u'こんにちは。私はＩＢＭのクラウドAI「WATSON」です。'
            control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声認識機能、機械翻訳機能、音声合成機能は、クラウドAI「WATSON」が処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'よろしくお願いします。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if (procText == 'microsoft' or procText == 'azure' or procText == 'azur') and (locked_ai == False):
        if  (qApiInp == 'azure') and (qApiTrn == qApiInp) and (qApiOut == qApiInp) \
        and (qLangOut == 'en') and (qLangTrn[:2] == qLangOut):
            speechtext = u'ja,hoya,既にマイクロソフトのクラウドAI「azure」で処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,マイクロソフトのクラウドAI「azure」に移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qLangTrn = 'en'
            qLangOut = qLangTrn[:2]

            qApiInp = 'azure'
            qApiTrn = 'azure'
            qApiOut = 'azure'
            speechtext = u'こんにちは。私はマイクロソフトのクラウドAI「azure」です。'
            control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声認識機能、機械翻訳機能、音声合成機能は、クラウドAI「azure」が処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'よろしくお願いします。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if ((procText == 'nict') or (procText == 'n i c t')) and (locked_ai == False):
        if  (qApiInp == 'nict') and (qApiTrn == qApiInp) and (qApiOut == qApiInp) \
        and (qLangOut == 'en') and (qLangTrn[:2] == qLangOut):
            speechtext = u'ja,hoya,既に情報通信研究機構「ＮＩＣＴ」のクラウドAIで処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,情報通信研究機構「ＮＩＣＴ」のクラウドAIに移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            #qLangTrn = 'en,fr,es,id,my,th,vi,zh,ko,'
            #qLangTrn = 'en,fr,es,id,zh,ko,'
            qLangTrn = 'en'

            qApiInp = 'nict'
            qApiTrn = 'nict'
            qApiOut = 'nict'
            speechtext = u'こんにちは。私は国立法人の情報通信研究機構「ＮＩＣＴ」のクラウドAIです。'
            control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声認識機能、機械翻訳機能、音声合成機能は、「ＮＩＣＴ」のクラウドAIが処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'よろしくお願いします。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if ((procText == 'contest') or (procText == 'contests') 
     or (procText == 'contesting possession')) \
    and (locked_ai == False):
        if  (qApiInp == 'google') and (qApiTrn == 'nict') \
        and ((qApiOut == 'watson') or (qApiOut == 'winos') or (qApiOut == 'macos')) \
        and (qLangOut == 'en') and (qLangTrn[:2] == qLangOut):
            speechtext = u'ja,hoya,既にＰＯＣコンテストモードで処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,ＰＯＣコンテストモードに移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            #qLangTrn = 'en,fr,es,id,my,th,vi,zh,ko,'
            #qLangTrn = 'en,fr,es,id,zh,ko,'
            qLangTrn = 'en,fr,zh,ko,'
            qLangOut = qLangTrn[:2]

            qApiInp = 'google'
            qApiTrn = 'nict'
            qApiOut = 'watson'
            if (qOS == 'windows'):
                qApiOut = 'winos'
            if (qOS == 'darwin'):
                qApiOut = 'macos'

            speechtext = u'こんにちは。私は国立法人の情報通信研究機構「ＮＩＣＴ」のクラウドAIです。'
            control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'機械翻訳機能は、「ＮＩＣＴ」のクラウドAIが処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声認識機能は、グーグルクラウドプラットホームのAIが処理します。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声合成機能は、WINDOWSのOSが処理します。'
            control_speech('04', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if (procText == 'presentation') and (locked_ai == False):
        if  (qApiInp == 'google') and (qApiTrn == 'nict') \
        and (qApiOut == 'none') \
        and (qLangOut == 'en') and (qLangTrn[:2] == qLangOut):
            speechtext = u'ja,hoya,既にプレゼンテーションモードで処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,プレゼンテーションモードに移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            #qLangTrn = 'en,fr,es,id,my,th,vi,zh,ko,'
            #qLangTrn = 'en,fr,es,id,zh,ko,'
            qLangTrn = 'en,fr,zh,ko,'
            qLangOut = qLangTrn[:2]

            qApiInp = 'google'
            qApiTrn = 'nict'
            qApiOut = 'nict'

            speechtext = u'こんにちは。私は国立法人の情報通信研究機構「ＮＩＣＴ」のクラウドAIです。'
            control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'機械翻訳機能は、「ＮＩＣＴ」のクラウドAIが処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声認識機能は、グーグルクラウドプラットホームのAIが処理します。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声合成機能は、停止します。'
            control_speech('04', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'プレゼンテーションの準備ＯＫです。スタンバイしています。'
            control_speech('04', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qApiOut = 'none'



    if ((procText == 'docomo')) and (locked_ai == False):
        if  (qApiInp == 'docomo'):
            speechtext = u'ja,hoya,既に「ドコモ」の音声認識機能で処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,「ドコモ」の音声認識機能に移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qLangTrn = 'en'
            qLangOut = qLangTrn[:2]

            qApiInp = 'docomo'
            qApiOut = 'free'
            if (qOS == 'windows'):
                qApiOut = 'winos'
            if (qOS == 'darwin'):
                qApiOut = 'macos'

            speechtext = u'こんにちは。私は「ドコモ」のクラウドAIです。'
            control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声認識機能は、「ドコモ」のクラウドAIが処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'よろしくお願いします。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if ((procText == 'winos') or (procText == 'windows')) and (qOS == 'windows') and (locked_ai == False):
        if  (qApiOut == 'winos'):
            speechtext = u'ja,hoya,既にWINDOWSのOSの音声合成機能で処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,WINDOWSのOSの音声合成機能に移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qLangTrn = 'en'
            qLangOut = qLangTrn[:2]

            qApiOut = 'winos'

            speechtext = u'こんにちは。私はWINDOWSのOSです。'
            control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声合成機能は、WINDOWSのOSが処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'よろしくお願いします。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if ((procText == 'macos') or (procText == 'osx')) and (qOS == 'darwin') and (locked_ai == False):
        if  (qApiOut == 'macos'):
            speechtext = u'ja,hoya,既にMACのOSの音声合成機能で処理中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,MACのOSの音声合成機能に移行します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qLangTrn = 'en'
            qLangOut = qLangTrn[:2]

            qApiOut = 'macos'

            speechtext = u'こんにちは。私はMACのOSです。'
            control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'音声合成機能は、MACのOSが処理します。'
            control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'よろしくお願いします。'
            control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )



    if (procText == 'audio stop') or (procText == 'voice stop'):
        if  (qApiOut == 'none'):
            speechtext = u'ja,hoya,既に音声合成機能は停止中です。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = u'ja,hoya,音声合成機能を停止します。'
            control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

            qApiOut = 'none'



    if ((procText == 'ai test') or (procText == 'api test')) and (locked_ai == False):

        qApiInp = 'docomo'
        qApiTrn = 'free'
        qApiOut = 'hoya'

        speechtext = u'ja,hoya,新しいクラウドAIのテストモードに移行します。'
        control_speech('00', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

        speechtext = u'音声認識機能は、docomoのクラウドAIが処理します。'
        control_speech('01', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'音声合成機能は、HOYAのクラウドAIが行います。'
        control_speech('02', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        speechtext = u'残念ながら日本語英語しか話せません。'
        control_speech('03', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, 'ja', speechtext, )
        speechtext = u'よろしくお願いします。'
        control_speech('04', fileId, runMode, micDev, qApiTrn, qApiOut, qLangInp, 'ja', speechtext, )

        qLangTrn = 'ja'
        qLangOut = qLangTrn[:2]



control_start=0
control_beat =0
control_busy =False
control_last =0
control_seq  =0
#control_web =False
def proc_control(cn_r, cn_s, ):
    global qOS
    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    global qBusyCtrl
    global qBusyInput
    global qBusySTT
    global qBusyTTS
    global qBusyPlay

    global control_start
    global control_beat
    global control_busy
    global control_last

    global control_seq
    global control_web

    qLogOutput('speechCtrl:init')

    runMode  = cn_r.get()
    micDev   = cn_r.get()
    micType  = cn_r.get()
    micGuide = cn_r.get()
    cn_r.task_done()

    qLogOutput('speechCtrl:runMode =' + str(runMode ))
    qLogOutput('speechCtrl:micDev  =' + str(micDev  ))
    qLogOutput('speechCtrl:micType =' + str(micType ))
    qLogOutput('speechCtrl:micGuide=' + str(micGuide))

    qLogOutput('speechCtrl:start')
    control_start=time.time()

    if (str(micDev) != 'file'):
        qBusySet(qBusyCtrl,  True)

        #qBusyCheck(qBusyCtrl , 3)
        #qBusyCheck(qBusySTT  , 3)
        #qBusyCheck(qBusyTTS  , 3)
        qBusyCheck(qBusyPlay , 3)
        if (micType == 'bluetooth') or (micGuide == 'on' or micGuide == 'sound'):
            qBusyCheck(qBusyInput , 3)

        speechtext = u'こんにちは。' + runMode + u'機能を起動しました。'
        control_speech('00', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    if (str(micDev) != 'file') and (runMode=='handsfree'):
        speechtext = '翻訳機能を起動しました。'
        control_speech('01', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

        if (micType == 'bluetooth'):
            speechtext = micType + u'マイク制御機能を起動しました。'
            control_speech('11', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
        else:
            speechtext = micType + u'マイク制御機能を起動しました。'
            control_speech('11', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'全ての機能が並列処理で起動しました。'
            control_speech('12', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
            speechtext = u'連続した音声入力が使用できます。'
            control_speech('13', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

        speechtext = u'vision start'
        control_sub(   '21', 'control', runMode, micDev, speechtext, 'en', )
        speechtext = u'play start'
        control_sub(   '22', 'control', runMode, micDev, speechtext, 'en', )
        time.sleep(20.00)

    if (str(micDev) != 'file'):
        speechtext = u'全ての準備が整いました。スタンバイしています。'
        control_speech('88', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )

    qBusySet(qBusyCtrl,  False)

    lasttext = ''
    lastlang = ''

    while (True):
        control_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('speechCtrl:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qLogOutput('speechCtrl: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                #control_last = time.time()
                cn_s.put(['PASS', ''])

            else:

                control_busy = True

                result = 'OK'

                path = qPathCtrl
                files = glob.glob(path + '*')
                if (len(files) > 0):

                    try:

                        for f in files:
                            file=f.replace('\\', '/')
                            if (file[-4:].lower() == '.txt' and file[-8:].lower() != '.tmp.txt'):
                                f1=file
                                f2=file[:-4] + '.tmp.txt'
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                            if (file[-8:].lower() == '.tmp.txt'):
                                f1=file
                                f2=file[:-8] + file[-4:]
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                                fileId = file.replace(path, '')
                                fileId = fileId[:-4]

                                control_seq += 1
                                if (control_seq >= 10000):
                                    control_seq = 1
                                seq4 = '{:04}'.format(control_seq)
                                seq2 = seq4[-2:]

                                wrkfile = qPathWork + 'control.' + seq2 + '.txt'
                                if (os.path.exists(wrkfile)):
                                    try:
                                        os.remove(wrkfile)
                                    except:
                                        pass

                                txt = ''
                                try:
                                    rt = codecs.open(file, 'r', 'utf-8')
                                    for t in rt:
                                        txt = (txt + ' ' + str(t)).strip()
                                    rt.close
                                    rt = None
                                except:
                                    rt = None

                                lang = ''
                                if (file[-7:] == '.ja.txt'):
                                    lang = 'ja'
                                if (file[-21:] == '.en.stt.translate.txt'):
                                    lang = 'en'

                                os.remove(file)

                                txt = str(txt).strip()

                                if (txt != '' and txt != '!'):
                                    if (txt == lasttext and lang == lastlang):
                                        if (runMode == 'debug'):
                                            qLogOutput('speechCtrl:(pass)' + txt + '(' + lang + ')')
                                    else:
                                        lasttext=txt
                                        lastlang=lang
                                        if (runMode == 'debug'):
                                            qLogOutput('speechCtrl:(exec)' + txt + '(' + lang + ')')

                                        try:
                                            w = codecs.open(wrkfile, 'w', 'utf-8')
                                            w.write(txt)
                                            w.close()
                                            w = None
                                        except:
                                            w = None

                                if (os.path.exists(wrkfile)):

                                        control_last = time.time()

                                        if (qOS == 'windows'):
                                            sendkey = subprocess.Popen(['python', '_speech_a3_sendmessage.py', wrkfile, ], )
                                            #sendkey.wait()
                                            #sendkey.terminate()
                                            #sendkey = None

                                        if (runMode=='debug') or (runMode=='handsfree'):
                                            if (txt == u'デモ紹介') or (txt == u'デモンストレーション'):
                                                speechtext = u'reset'
                                                control_sub(   '00', 'control', runMode, micDev, speechtext, 'en', )
                                                speechtext = u'default'
                                                control_sub(   '01', 'control', runMode, micDev, speechtext, 'en', )
                                                time.sleep( 3.00)

                                        if (runMode=='debug') or (runMode=='handsfree'):
                                            if (txt == u'システム終了' or txt == u'バルス'):
                                                speechtext = u'システム終了プロセスを開始しました。'
                                                control_speech('90', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
                                                time.sleep( 3.00)

                                        control_sub(seq4, fileId, runMode, micDev, txt, lang, )

                                        if (runMode=='debug') or (runMode=='handsfree'):
                                            if (txt == u'システム終了' or txt == u'バルス'):
                                                speechtext = runMode + u'機能を終了しました。'
                                                control_speech('91', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
                                                time.sleep(10.00)
                                                speechtext = u'さようなら。また、よろしくお願いします。'
                                                control_speech('99', 'control', runMode, micDev, qApiTrn, qApiOut, qLangInp, qLangOut, speechtext, )
                                                cn_s.put(['END', ''])
                                                time.sleep( 5.00)
                                                break

                    except:
                        pass
                        result = 'NG'

                #if (str(micDev) == 'file'):
                #    if (result == 'OK'):
                #        cn_s.put(['END', ''])
                #        time.sleep( 5.00)
                #        break
                #    else:
                #        cn_s.put(['ERROR', ''])
                #        time.sleep( 5.00)
                #        break
                #else:
                cn_s.put([result, ''])

        control_busy = False
        qBusySet(qBusyCtrl, False)

        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.10)

    qLogOutput('speechCtrl:terminate')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('speechCtrl:end')



def stt_sub(seq, fileId, runMode, micDev, file, ):
    global qApiInp
    global qApiTrn
    global qApiOut
    global qLangInp
    global qLangTrn
    global qLangTxt
    global qLangOut

    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    if (runMode == 'handsfree') or (runMode == 'translator'):
        inpInput = file
        inpOutput= qPathSTT  + fileId + '.' + qLangInp + '.txt'
        trnInput = inpOutput
        trnOutput= qPathTRA  + fileId + '.' + qLangInp + '.' + qLangTrn[:2] + '.stt.translate.txt'
        txtInput = ''
        txtOutput= ''
        outInput = trnOutput
        outOutput= qPathPlay + fileId + '.' + qLangOut + '.voice.mp3'
        inpPlay  = 'off'
        txtPlay  = 'off'
        outPlay  = 'off'

    if (runMode == 'debug') or (runMode == 'learning'):
        inpInput = file
        inpOutput= qPathSTT  + fileId + '.' + qLangInp + '.txt'
        trnInput = inpOutput
        trnOutput= qPathTRA  + fileId + '.' + qLangInp + '.' + qLangTrn[:2] + '.stt.translate.txt'
        txtInput = inpOutput
        txtOutput= qPathPlay + fileId + '.' + qLangOut + '.feedback.mp3'
        outInput = trnOutput
        outOutput= qPathPlay + fileId + '.' + qLangOut + '.voice.mp3'
        qLangTxt  = qLangInp
        inpPlay  = 'off'
        txtPlay  = 'off'
        outPlay  = 'off'

    if (runMode == 'speech') or (runMode == 'number'):
        inpInput = file
        inpOutput= qPathSTT  + fileId + '.' + qLangInp + '.txt'
        trnInput = ''
        trnOutput= ''
        if (micDev != 'file'):
            trnInput = inpOutput
            trnOutput= qPathTRA  + fileId + '.' + qLangInp + '.' + qLangTrn[:2] + '.stt.translate.txt'
        txtInput = ''
        txtOutput= ''
        outInput = ''
        outOutput= ''
        inpPlay  = 'off'
        txtPlay  = 'off'
        outPlay  = 'off'

    if (qApiOut == 'none'):
        txtOutput= ''
        outOutput= ''



    if (True):
        api = subprocess.Popen(['python', '_speech_a3_all_api.py', \
              runMode, micDev, qApiInp, qApiTrn, qApiOut, qLangInp, qLangTrn, qLangTxt, qLangOut, \
              'STT'+str(seq), fileId, inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput, \
              inpPlay, txtPlay, outPlay, ], \
              )
        #api.wait()
        #api.terminate()
        #api = None

        time.sleep(3.00)
        if (str(micDev) == 'file'):
            if (seq[-1:] == '0'):
                 api.wait()
                 api.terminate()
                 api = None
                 time.sleep(20.00)



sttcore_start=0
sttcore_beat =0
sttcore_busy =False
sttcore_last =0
sttcore_seq  =0
def proc_sttcore(cn_r, cn_s, ):
    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    global qBusyCtrl
    global qBusyInput
    global qBusySTT
    global qBusyTTS
    global qBusyPlay

    global sttcore_start
    global sttcore_beat
    global sttcore_busy
    global sttcore_last

    global sttcore_seq

    qLogOutput('stt_core__:init')

    runMode  = cn_r.get()
    micDev   = cn_r.get()
    micType  = cn_r.get()
    micGuide = cn_r.get()
    cn_r.task_done()

    qLogOutput('stt_core__:runMode =' + str(runMode ))
    qLogOutput('stt_core__:micDev  =' + str(micDev  ))
    qLogOutput('stt_core__:micType =' + str(micType ))
    qLogOutput('stt_core__:micGuide=' + str(micGuide))

    qLogOutput('stt_core__:start')
    sttcore_start=time.time()

    while (True):
        sttcore_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('stt_core__:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qLogOutput('stt_core__: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                #sttcore_last = time.time()
                cn_s.put(['PASS', ''])

            else:

                sttcore_busy = True

                result = 'OK'

                path = qPathWav
                files = glob.glob(path + '*')
                if (len(files) > 0):
                    qBusySet(qBusySTT, True)

                    if (str(micDev) == 'file'):
                        for f in files:
                            qLogOutput(f)

                    qBusyCheck(qBusyCtrl  , 3)
                    #qBusyCheck(qBusySTT  , 3)
                    #qBusyCheck(qBusyTTS  , 3)
                    #qBusyCheck(qBusyPlay , 3)
                    if (micType == 'bluetooth') or (micGuide == 'on' or micGuide == 'sound'):
                        qBusyCheck(qBusyInput , 3)

                files = glob.glob(path + '*')
                if (len(files) > 0):

                     try:

                        for f in files:
                            file=f.replace('\\', '/')
                            if (file[-4:].lower() == '.wav' and file[-8:].lower() != '.tmp.wav'):
                                f1=file
                                f2=file[:-4] + '.tmp.wav'
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass
                            if (file[-4:].lower() == '.mp3' and file[-8:].lower() != '.tmp.mp3'):
                                f1=file
                                f2=file[:-4] + '.tmp.mp3'
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                            if (file[-8:].lower() == '.tmp.wav' or file[-8:].lower() == '.tmp.mp3'):
                                f1=file
                                f2=file[:-8] + file[-4:]
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                                fileId = file.replace(path, '')
                                fileId = fileId[:-4]

                                sttcore_seq += 1
                                if (sttcore_seq >= 10000):
                                    sttcore_seq = 1
                                seq4 = '{:04}'.format(sttcore_seq)
                                seq2 = seq4[-2:]

                                wrkfile = qPathWork + 'sttcore.' + seq2 + '.wav'
                                if (os.path.exists(wrkfile)):
                                    try:
                                        os.remove(wrkfile)
                                    except:
                                        pass

                                sox = subprocess.Popen(['sox', '-q', file, '-r', '16000', '-b', '16', '-c', '1', wrkfile, ], \
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                                sox.wait()
                                sox.terminate()
                                sox = None

                                if (str(micDev) != 'file'):
                                    os.remove(file)

                                if (os.path.exists(wrkfile)):

                                    if (micDev == 'file'):
                                        qLogOutput('')
                                        qLogOutput('stt_core__:' + fileId + u' → ' + wrkfile[:-4])

                                    sttcore_last = time.time()

                                    stt_sub(seq4, fileId, runMode, micDev, wrkfile, )

                     except:
                        pass
                        result = 'NG'

                if (str(micDev) == 'file'):
                    if (result == 'OK'):
                        cn_s.put(['END', ''])
                        time.sleep( 5.00)
                        break
                    else:
                        cn_s.put(['ERROR', ''])
                        time.sleep( 5.00)
                        break
                else:
                    cn_s.put([result, ''])

        sttcore_busy = False
        qBusySet(qBusySTT, False)

        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.10)

    qLogOutput('stt_core__:terminate')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('stt_core__:end')



def tts_sub(seq, fileId, runMode, micDev, file, txtText, ):
    global qApiInp
    global qApiTrn
    global qApiOut
    global qLangInp
    global qLangTrn
    global qLangTxt
    global qLangOut

    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    inpLang = qLangTxt
    trnLang = qLangTrn
    outLang = qLangOut
    while (txtText[:3] == 'ja,' or txtText[:3] == 'en,'):
        inpLang = txtText[:2]
        trnLang = txtText[:2]
        outLang = txtText[:2]
        txtText = txtText[3:]

    if (inpLang != trnLang) or (inpLang != outLang):
        inpInput = ''
        inpOutput= ''
        trnInput = file
        trnOutput= qPathTRA  + fileId + '.' + inpLang + '.' + trnLang[:2] + '.tts.translate.txt'
        txtInput = ''
        txtOutput= ''
        outInput = trnOutput
        outOutput= qPathPlay + fileId + '.' + outLang + '.voice.mp3'
        inpPlay  = 'off'
        txtPlay  = 'off'
        outPlay  = 'off'
    else:
        inpInput = ''
        inpOutput= ''
        trnInput = ''
        trnOutput= ''
        txtInput = file
        txtOutput= qPathPlay + fileId + '.' + inpLang + '.' + inpLang + '.mp3'
        outInput = ''
        outOutput= ''
        inpPlay  = 'off'
        txtPlay  = 'off'
        outPlay  = 'off'

    if (qApiOut == 'none'):
        txtOutput= ''
        outOutput= ''

    if (True):
        api = subprocess.Popen(['python', '_speech_a3_all_api.py', \
              #runMode, micDev, qApiInp, qApiTrn, qApiOut, qLangInp, qLangTrn, qLangTxt, qLangOut, \
              runMode, micDev, qApiInp, qApiTrn, qApiOut, qLangTxt, qLangTrn, qLangTxt, qLangOut, \
              'TTS'+str(seq), fileId, inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput, \
              inpPlay, txtPlay, outPlay, ], \
              )
        #api.wait()
        #api.terminate()
        #api = None

        time.sleep(2.00)
        if (str(micDev) == 'file'):
            if (seq[-1:] == '0'):
                 api.wait()
                 api.terminate()
                 api = None
                 time.sleep(5.00)



ttscore_start=0
ttscore_beat =0
ttscore_busy =False
ttscore_last =0
ttscore_seq  =0
def proc_ttscore(cn_r, cn_s, ):
    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    global qBusyCtrl
    global qBusyInput
    global qBusySTT
    global qBusyTTS
    global qBusyPlay

    global ttscore_start
    global ttscore_beat
    global ttscore_busy
    global ttscore_last

    global ttscore_seq

    qLogOutput('tts_core__:init')

    runMode  = cn_r.get()
    micDev   = cn_r.get()
    micType  = cn_r.get()
    micGuide = cn_r.get()
    cn_r.task_done()

    qLogOutput('tts_core__:runMode =' + str(runMode ))
    qLogOutput('tts_core__:micDev  =' + str(micDev  ))
    qLogOutput('tts_core__:micType =' + str(micType ))
    qLogOutput('tts_core__:micGuide=' + str(micGuide))

    qLogOutput('tts_core__:start')
    ttscore_start=time.time()

    while (True):
        ttscore_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('tts_core__:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qLogOutput('tts_core__: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                #ttscore_last = time.time()
                cn_s.put(['PASS', ''])

            else:

                ttscore_busy = True

                result = 'OK'

                path = qPathTTS
                files = glob.glob(path + '*')
                if (len(files) > 0):
                    qBusySet(qBusyTTS, True)

                    if (str(micDev) == 'file'):
                        for f in files:
                            qLogOutput(f)

                    #qBusyCheck(qBusyCtrl , 3)
                    #qBusyCheck(qBusyTTS  , 3)
                    #qBusyCheck(qBusySTT  , 3)
                    #qBusyCheck(qBusyPlay , 3)
                    if (micType == 'bluetooth') or (micGuide == 'on' or micGuide == 'sound'):
                        qBusyCheck(qBusyInput , 3)

                files = glob.glob(path + '*')
                if (len(files) > 0):

                    try:

                        for f in files:
                            file=f.replace('\\', '/')
                            if (file[-4:].lower() == '.txt' and file[-8:].lower() != '.tmp.txt'):
                                f1=file
                                f2=file[:-4] + '.tmp.txt'
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                            if (file[-8:].lower() == '.tmp.txt'):
                                f1=file
                                f2=file[:-8] + file[-4:]
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                                fileId = file.replace(path, '')
                                fileId = fileId[:-4]

                                ttscore_seq += 1
                                if (ttscore_seq >= 10000):
                                    ttscore_seq = 1
                                seq4 = '{:04}'.format(ttscore_seq)
                                seq2 = seq4[-2:]

                                wrkfile = qPathWork + 'ttscore.' + seq2 + '.txt'
                                if (os.path.exists(wrkfile)):
                                    try:
                                        os.remove(wrkfile)
                                    except:
                                        pass

                                txt = ''
                                try:
                                    rt = codecs.open(file, 'r', 'utf-8')
                                    for t in rt:
                                        txt = (txt + ' ' + str(t)).strip()
                                    rt.close
                                    rt = None
                                except:
                                    rt = None

                                txt = str(txt).strip()
                                if (txt != '' and txt != '!'):
                                    try:
                                        w = codecs.open(wrkfile, 'w', 'utf-8')
                                        w.write(txt)
                                        w.close()
                                        w = None
                                    except:
                                        w = None

                                if (str(micDev) != 'file'):
                                    os.remove(file)

                                if (os.path.exists(wrkfile)):

                                    if (micDev == 'file'):
                                        qLogOutput('')
                                        qLogOutput('tts_core__:' + fileId + u' → ' + wrkfile)

                                    ttscore_last = time.time()

                                    tts_sub(seq4, fileId, runMode, micDev, wrkfile, txt, )

                    except:
                        pass
                        result = 'NG'

                if (str(micDev) == 'file'):
                    if (result == 'OK'):
                        cn_s.put(['END', ''])
                        time.sleep( 5.00)
                        break
                    else:
                        cn_s.put(['ERROR', ''])
                        time.sleep( 5.00)
                        break
                else:
                    cn_s.put([result, ''])

        ttscore_busy = False
        qBusySet(qBusyTTS, False)

        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.10)

    qLogOutput('tts_core__:terminate')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('tts_core__:end')



def main_init(runMode, micDev, ):
    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    global qBusyCtrl
    global qBusyInput
    global qBusySTT
    global qBusyTTS
    global qBusyPlay

    global qCtrlBgm
    global qCtrlWeb
    global qCtrlChatting
    global qCtrlKnowledge
    global qCtrlVision
    global qCtrlRecognize
    global qCtrlTranslate
    
    qMakeDirs('temp/_log/',   False)
    qMakeDirs('temp/_cache/', False)

    if (str(micDev) != 'file'):
        qMakeDirs(qPathCtrl, True )
        qMakeDirs(qPathInp,  True )
        qMakeDirs(qPathWav,  True )
        qMakeDirs(qPathSTT,  True )
        qMakeDirs(qPathTTS,  True )
        qMakeDirs(qPathTRA,  True )
        qMakeDirs(qPathPlay, True )
        qMakeDirs(qPathRec,  False)
        qMakeDirs(qPathWork, True )
    else:
        qMakeDirs(qPathCtrl, True )
        qMakeDirs(qPathInp,  False)
        qMakeDirs(qPathWav,  True )
        qMakeDirs(qPathSTT,  True )
        qMakeDirs(qPathTTS,  False)
        qMakeDirs(qPathTRA,  True )
        qMakeDirs(qPathPlay, True )
        qMakeDirs(qPathRec,  False)
        qMakeDirs(qPathWork, True )

    qBusySet(qBusyCtrl,  False )
    qBusySet(qBusyInput, False )
    qBusySet(qBusySTT,   False )
    qBusySet(qBusyTTS,   False )
    qBusySet(qBusyPlay,  False )

    qBusySet(qCtrlBgm,       False )
    qBusySet(qCtrlWeb,       False )
    qBusySet(qCtrlChatting,  False )
    qBusySet(qCtrlKnowledge, False )
    qBusySet(qCtrlVision,    False )
    qBusySet(qCtrlRecognize, False )
    qBusySet(qCtrlTranslate, False )



main_start=0
main_beat =0
main_busy =False
main_last =0
if (__name__ == '__main__'):
    #global main_beat
    #global sttcore_beat

    qLogOutput('___main___:init')
    qLogOutput('___main___:exsample.py runMode, api..., lang..., micDev, micType, micGuide, micLevel, path..., ')
    #runMode  handsfree, translator, speech, ...,
    #         knowledge, learning, number,
    #api      free, google, watson, azure, nict, winos, macos, docomo,
    #lang     ja, en, fr, kr...
    #micDev   num or file
    #micType  usb or bluetooth
    #micGuide off, on, display, sound

    runMode  = 'handsfree'

    micDev   = '0'
    micType  = 'bluetooth'
    micGuide = 'on'
    micLevel = '0'

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()

    if (len(sys.argv) >= 3):
        micDev   = str(sys.argv[2]).lower()
        if (str(micDev) == 'file'):
           micGuide = 'off' 
    if (len(sys.argv) >= 4):
        micType  = str(sys.argv[3]).lower()
    if (len(sys.argv) >= 5):
        micGuide = str(sys.argv[4]).lower()
    if (len(sys.argv) >= 6):
        p = str(sys.argv[5]).lower()
        if (p.isdigit() and p != '0'):
            micLevel = p

    if (len(sys.argv) >= 7):
        qApiInp  = str(sys.argv[6]).lower()
        if (qApiInp == 'google') or (qApiInp == 'watson') \
        or (qApiInp == 'azure')  or (qApiInp == 'nict'):
            qApiTrn  = qApiInp
            qApiOut  = qApiInp
        else:
            qApiTrn  = 'free'
            qApiOut  = 'free'
        if (qApiInp == 'nict'):
            #qLangTrn = 'en,fr,es,id,my,th,vi,zh,ko,'
            qLangTrn = 'en,fr,es,id,zh,ko,'
            qLangOut = qLangTrn[:2]
    if (len(sys.argv) >= 8):
        qApiTrn  = str(sys.argv[7]).lower()
    if (len(sys.argv) >= 9):
        qApiOut  = str(sys.argv[8]).lower()
    if (len(sys.argv) >= 10):
        qLangInp = str(sys.argv[9]).lower()
        qLangTxt = qLangInp
    if (len(sys.argv) >= 11):
        qLangTrn = str(sys.argv[10]).lower()
        qLangOut = qLangTrn[:2]
    if (len(sys.argv) >= 12):
        qLangTxt = str(sys.argv[11]).lower()
    if (len(sys.argv) >= 13):
        qLangOut = str(sys.argv[12]).lower()

    qLogOutput('')
    qLogOutput('___main___:runMode  =' + str(runMode  ))
    qLogOutput('___main___:micDev   =' + str(micDev   ))
    qLogOutput('___main___:micType  =' + str(micType  ))
    qLogOutput('___main___:micGuide =' + str(micGuide ))
    qLogOutput('___main___:micLevel =' + str(micLevel ))

    qLogOutput('___main___:qApiInp  =' + str(qApiInp  ))
    qLogOutput('___main___:qApiTrn  =' + str(qApiTrn  ))
    qLogOutput('___main___:qApiOut  =' + str(qApiOut  ))
    qLogOutput('___main___:qLangInp =' + str(qLangInp ))
    qLogOutput('___main___:qLangTrn =' + str(qLangTrn ))
    qLogOutput('___main___:qLangTxt =' + str(qLangTxt ))
    qLogOutput('___main___:qLangOut =' + str(qLangOut ))

    main_init(runMode, micDev, )

    if (True):
        qLogOutput('')
        voice2wav = subprocess.Popen(['python', '_speech_a3_voice2wav.py', \
                    runMode, micDev, micType, micGuide, micLevel, \
                    ], )
                    #], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
                    #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        time.sleep(2.00)
        if (str(micDev) == 'file'):
            voice2wav.wait()
            voice2wav.terminate()
            voice2wav = None

        qLogOutput('')
        playvoice = subprocess.Popen(['python', '_speech_a3_playvoice.py', \
                    runMode, micDev, micType, micGuide, micLevel, \
                    ], )
                    #], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
                    #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        time.sleep(2.00)

    qLogOutput('')
    qLogOutput('___main___:start')
    main_start     = time.time()
    main_beat      = 0

    control_s      = queue.Queue()
    control_r      = queue.Queue()
    control_proc   = None
    control_beat   = 0
    control_pass   = 0

    sttcore_s      = queue.Queue()
    sttcore_r      = queue.Queue()
    sttcore_proc   = None
    sttcore_beat   = 0
    sttcore_pass   = 0

    ttscore_s      = queue.Queue()
    ttscore_r      = queue.Queue()
    ttscore_proc   = None
    ttscore_beat   = 0
    ttscore_pass   = 0

    while (True):
        main_beat = time.time()

        # check sttcore_last and ttscore_last

        if (str(micDev) == 'file'):
            if (sttcore_last == 0):
                sttcore_last = time.time()
            if (ttscore_last == 0):
                ttscore_last = time.time()
            sec1 = int(time.time() - sttcore_last)
            sec2 = int(time.time() - ttscore_last)
            if (sec1 > 240 and sec2 > 240):
                break

        # Thread timeout check

        if (control_beat != 0):
          if (str(micDev) != 'file'):
            sec = int(time.time() - control_beat)
            if (sec > 60):
                qLogOutput('___main___:control_proc 60s')
                qLogOutput('___main___:control_proc break')
                control_s.put([None, None])
                time.sleep(3.00)
                control_proc = None
                control_beat = 0
                control_pass = 0

        if (sttcore_beat != 0):
          if (str(micDev) != 'file'):
            sec = int(time.time() - sttcore_beat)
            if (sec > 60):
                qLogOutput('___main___:sttcore_proc 60s')
                qLogOutput('___main___:sttcore_proc break')
                sttcore_s.put([None, None])
                time.sleep(3.00)
                sttcore_proc = None
                sttcore_beat = 0
                sttcore_pass = 0

        if (ttscore_beat != 0):
          if (str(micDev) != 'file'):
            sec = int(time.time() - ttscore_beat)
            if (sec > 60):
                qLogOutput('___main___:ttscore_proc 60s')
                qLogOutput('___main___:ttscore_proc break')
                ttscore_s.put([None, None])
                time.sleep(3.00)
                ttscore_proc = None
                ttscore_beat = 0
                ttscore_pass = 0

        # Thread start

        if (control_proc is None):
            while (control_s.qsize() > 0):
                dummy = control_s.get()
            while (control_r.qsize() > 0):
                dummy = control_r.get()
            control_proc = threading.Thread(target=proc_control, args=(control_s,control_r,))
            control_proc.daemon = True
            control_s.put(runMode )
            control_s.put(micDev  )
            control_s.put(micType )
            control_s.put(micGuide)
            control_proc.start()
            time.sleep(1.00)

            control_s.put(['START', ''])

        if (sttcore_proc is None):
            while (sttcore_s.qsize() > 0):
                dummy = sttcore_s.get()
            while (sttcore_r.qsize() > 0):
                dummy = sttcore_r.get()
            sttcore_proc = threading.Thread(target=proc_sttcore, args=(sttcore_s,sttcore_r,))
            sttcore_proc.daemon = True
            sttcore_s.put(runMode )
            sttcore_s.put(micDev  )
            sttcore_s.put(micType )
            sttcore_s.put(micGuide)
            sttcore_proc.start()
            time.sleep(1.00)

            sttcore_s.put(['START', ''])

        if (ttscore_proc is None):
            while (ttscore_s.qsize() > 0):
                dummy = ttscore_s.get()
            while (ttscore_r.qsize() > 0):
                dummy = ttscore_r.get()
            ttscore_proc = threading.Thread(target=proc_ttscore, args=(ttscore_s,ttscore_r,))
            ttscore_proc.daemon = True
            ttscore_s.put(runMode )
            ttscore_s.put(micDev  )
            ttscore_s.put(micType )
            ttscore_s.put(micGuide)
            ttscore_proc.start()
            time.sleep(1.00)

            ttscore_s.put(['START', ''])

        # processing

        if (control_r.qsize() == 0 and control_s.qsize() == 0):
            control_s.put(['PROC', ''])
            control_pass += 1
        else:
            control_pass = 0
        if (control_pass > 50):
            control_s.put(['PASS', ''])
            control_pass = 0

        break_flag = False
        while (control_r.qsize() > 0):
            control_get = control_r.get()
            control_res = control_get[0]
            control_dat = control_get[1]
            control_r.task_done()
            if (control_res == 'END'):
                break_flag = True
            if (control_res == 'ERROR'):
                break_flag = True
        if (break_flag == True):
            break
            
        if (sttcore_r.qsize() == 0 and sttcore_s.qsize() == 0):
            sttcore_s.put(['PROC', ''])
            sttcore_pass += 1
        else:
            sttcore_pass = 0
        if (sttcore_pass > 50):
            sttcore_s.put(['PASS', ''])
            sttcore_pass = 0

        while (sttcore_r.qsize() > 0):
            sttcore_get = sttcore_r.get()
            sttcore_res = sttcore_get[0]
            sttcore_dat = sttcore_get[1]
            sttcore_r.task_done()

        if (ttscore_r.qsize() == 0 and ttscore_s.qsize() == 0):
            ttscore_s.put(['PROC', ''])
            ttscore_pass += 1
        else:
            ttscore_pass = 0
        if (ttscore_pass > 50):
            ttscore_s.put(['PASS', ''])
            ttscore_pass = 0

        while (ttscore_r.qsize() > 0):
            ttscore_get = ttscore_r.get()
            ttscore_res = ttscore_get[0]
            ttscore_dat = ttscore_get[1]
            ttscore_r.task_done()



        time.sleep(0.05)



    qLogOutput('')
    qLogOutput('___main___:terminate')

    try:
        control_s.put( [None, None] )
        sttcore_s.put( [None, None] )
        ttscore_s.put( [None, None] )
        time.sleep(3.00)
    except:
        pass

    if (not voice2wav is None):
        voice2wav.terminate()
        voice2wav = None
    if (not playvoice is None):
        playvoice.terminate()
        playvoice = None

    try:
        control_proc.join()
        sttcore_proc.join()
        ttscore_proc.join()
    except:
        pass

    qBusySet(qBusyCtrl, False)
    qBusySet(qBusyTTS,  False)
    qBusySet(qBusySTT,  False)

    qLogOutput('___main___:bye!')


