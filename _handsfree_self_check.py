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



qPathCtrl  = 'temp/a3_0control/'
qPathInp   = 'temp/a3_1voice/'
qPathSTT   = 'temp/a3_3stt_txt/'
qPathTTS   = 'temp/a3_5tts_txt/'
qPathPlay  = 'temp/a3_7play_voice/'
qPathRec   = 'temp/a3_8recorder/'
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
            or (qBusyCheck(qBusyPlay ,0) == 'busy'):
                busy_flag = True
                time.sleep(0.10)
                break


def tts_speech(runMode, id, speechText, idolsec=2, maxwait=15, ):
    global qPathTTS

    speech_wait(idolsec,maxwait)

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
        id  = 'selfcheck.' + '{:02}'.format(seq)
        tts_speech(runMode, id, txt, 0, 0, )
        time.sleep(speech['wait'])

def loopback_speech(runMode, speech, lang='ja,hoya,', idolsec=2, maxwait=15, ):
    global qPathCtrl
    global qPathInp
    global qPathSTT
    global qPathTTS
    global qPathPlay
    global qPathRec
    global qPathWork

    xrunMode = runMode
    xmicDev  = '0'
    xApiInp  = 'free'
    xApiTrn  = 'free'
    xApiOut  = 'free'
    xLangInp = 'ja'
    xLangTrn = 'en'
    xLangTxt = xLangInp
    xLangOut = xLangTrn

    speech_wait(idolsec,maxwait)

    if (True):
        seq='00'
        fileId = 'CHK' + seq
        speechtext = lang + speech

        now=datetime.datetime.now()
        stamp=now.strftime('%Y%m%d-%H%M%S')
        wrkText = qPathWork + stamp + '.' + seq + '.selfcheck.txt'
        wrkOut  = qPathWork + stamp + '.' + seq + '.selfcheck.mp3'

        try:
            w = codecs.open(wrkText, 'w', 'utf-8')
            w.write(speechtext)
            w.close()
            w = None
        except:
            w = None

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

        api = subprocess.Popen(['python', '_speech_a3_all_api.py', \
              xrunMode, xmicDev, xApiInp, xApiTrn, xApiOut, xLangInp, xLangTrn, xLangTxt, xLangOut, \
              str(seq), fileId, inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput, \
              inpPlay, txtPlay, outPlay, qPathCtrl, qPathSTT, qPathTTS, qPathRec, qPathWork, ], \
              )
        api.wait()
        api.terminate()
        api = None

        if (os.path.exists(wrkOut)):
            wrkPlay = qPathPlay + stamp + '.' + fileId + '.mp3'
            shutil.copy2(wrkOut, wrkPlay)
            wrkInput = qPathInp + stamp + '.' + fileId + '.mp3'
            shutil.copy2(wrkOut, wrkInput)

            time.sleep(3.00)
            speech_wait(idolsec=3,maxwait=60)

            return wrkOut

    return False



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
    qLogOutput('self_check:init')
    qLogOutput('self_check:exsample.py runMode,')

    runMode = 'debug'
    check   = 'all'

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        check    = sys.argv[2]

    #check   = 'demo'

    qLogOutput('self_check:runMode  =' + str(runMode  ))
    qLogOutput('self_check:check    =' + str(check    ))

    qLogOutput('')
    qLogOutput('self_check:start')

    lang = 'ja,hoya,'



    if (check == 'all') or (check == 'demo'):
        text = u'BGM'
        #loopback_speech(runMode, text, lang, )
        loopback_speech(runMode, text, 'ja,free,', )

        text = u'画像処理の開始'
        #loopback_speech(runMode, text, lang, )
        loopback_speech(runMode, text, 'ja,free,', )

        text = u'プレイリスト 0'
        #loopback_speech(runMode, text, lang, )
        loopback_speech(runMode, text, 'ja,free,', )

        speech_wait(idolsec=5,maxwait=30, )

        speechs = []
        speechs.append({'text':u'こんにちは。私はハンズフリーコントロール翻訳システムです。', 'wait':0, })
        speechs.append({'text':u'私は、近藤家の自家用車ＭＰＶで動作するように設計されました。', 'wait':0, })
        speechs.append({'text':u'これから自己診断を兼ねて、私自身の機能紹介を行います。', 'wait':0, })
        speechs.append({'text':u'このナレーションは、主にＨＯＹＡの音声合成ＡＩが担当します。', 'wait':0, })
        speechs.append({'text':u'よろしくお願いします。', 'wait':0, })
        speech_run(runMode, speechs, lang, )
        speechs = []
        speechs.append({'text':u'こんにちは。私はハンズフリーコントロール翻訳システムです。', 'wait':0, })
        speechs.append({'text':u'これから自己診断を兼ねて、私自身の機能紹介を行います。', 'wait':0, })
        speechs.append({'text':u'よろしくお願いします。', 'wait':0, })
        speech_run(runMode, speechs, ''  , )



    if (check == 'all') or (check == u'翻訳') or (check == 'demo'):

        speechs = []
        speechs.append({'text':u'翻訳機能', 'wait':0, })
        speechs.append({'text':u'音声認識、機械翻訳、音声合成機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'それでは、翻訳機能の自己テストを開始します。', 'wait':0, })
        speech_run(runMode, speechs, lang, )

        text = u'A.P.I.一覧。'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

    if (check == 'all') or (check == u'翻訳') or (check == 'demo'):

        text = u'スペシャル。'
        #loopback_speech(runMode, text, lang, )
        loopback_speech(runMode, text, 'ja,free,', )

        speech_wait(idolsec=5,maxwait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            loopback_speech(runMode, text, lang, )

        text = u'コンテスト。'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            loopback_speech(runMode, text, lang, )

    if (check == 'all') or (check == u'翻訳'):
        speech_wait(idolsec=5,maxwait=30, )

        text = u'n.i.c.t.'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            loopback_speech(runMode, text, lang, )

        text = u'アイビーエム。'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            loopback_speech(runMode, text, lang, )

        text = u'マイクロソフト。'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            loopback_speech(runMode, text, lang, )

        text = u'グーグル。'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            loopback_speech(runMode, text, lang, )

        text = u'デフォルト。'
        #loopback_speech(runMode, text, lang, )
        loopback_speech(runMode, text, 'ja,free,', )

        speech_wait(idolsec=5,maxwait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            loopback_speech(runMode, text, lang, )



    if (check == 'all') or (check == u'翻訳') or (check == 'demo'):

        text = u'言語は何ですか？'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'フランス語。'
        loopback_speech(runMode, text, lang, )

        text = u'2020年。日本で逢いましょう。'
        loopback_speech(runMode, text, lang, )

        text = u'英語。'
        loopback_speech(runMode, text, 'ja,free,', )

        speechs = []
        speechs.append({'text':u'翻訳機能の紹介を終わります。', 'wait':0, })
        speech_run(runMode, speechs, lang, )
        speech_run(runMode, speechs, ''  , )



    if (check == 'all') or (check == u'ハンズフリー') or (check == 'demo'):
        speech_wait(idolsec=5,maxwait=30, )

        speechs = []
        speechs.append({'text':u'ハンズフリー制御', 'wait':0, })
        speechs.append({'text':u'ハンズフリー制御機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'この翻訳システムで対処できない場合、外部のデバイスと連携します。', 'wait':0, })
        if (check == 'demo'):
            speechs.append({'text':u'デモンストレーションでは、ＢＧＭの制御機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'それでは、ハンズフリー機能の自己テストを開始します。', 'wait':0, })
        speech_run(runMode, speechs, lang, )
        speechs = []
        speechs.append({'text':u'ハンズフリー機能', 'wait':0, })
        speechs.append({'text':u'ハンズフリー機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'それでは、ハンズフリー機能の自己テストを開始します。', 'wait':0, })
        speech_run(runMode, speechs, ''  , )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'プレイリスト。一覧。'
        #loopback_speech(runMode, text, lang, )
        loopback_speech(runMode, text, 'ja,free,', )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'bgm'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'bgm。ストップ。'
        loopback_speech(runMode, text, lang, )

        text = u'三木市の天気。'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

    if (check == 'all') or (check == u'ハンズフリー'):

        text = u'姫路市のニュース。'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'岡山大学の住所を調べて？'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'ブラウザー。'
        loopback_speech(runMode, text, lang, )

        text = u'岡山大学。'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'ブラウザー。ストップ。'
        loopback_speech(runMode, text, lang, )

        text = u'知識データベース開始。'
        loopback_speech(runMode, text, lang, )

        text = u'富士山の高さは？'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'知識データベース終了。'
        loopback_speech(runMode, text, lang, )

        text = u'雑談開始。'
        loopback_speech(runMode, text, lang, )

        text = u'富士山の高さ知ってる？'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'雑談終了。'
        loopback_speech(runMode, text, lang, )

        text = u'ここの住所調べて？'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'ここから姫路城の経路調べて？'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

        text = u'アミに電話して。'
        loopback_speech(runMode, text, lang, )

        speech_wait(idolsec=5,maxwait=30, )

    if (check == 'all') or (check == u'ハンズフリー') or (check == 'demo'):

        speechs = []
        speechs.append({'text':u'ハンズフリー制御機能の紹介を終わります。', 'wait':0, })
        speech_run(runMode, speechs, lang, )
        speech_run(runMode, speechs, ''  , )



    if (check == 'all') or (check == u'連携') or (check == 'demo'):
        speech_wait(idolsec=5,maxwait=30, )

        speechs = []
        speechs.append({'text':u'外部ＡＩ連携機能', 'wait':0, })
        speechs.append({'text':u'スマートスピーカー等の外部機器との連携機能を紹介します。', 'wait':0, })
        if (check == 'demo'):
            speechs.append({'text':u'デモンストレーションでは、アイフォーンのSiriに連携します。', 'wait':0, })
        speechs.append({'text':u'それでは、外部ＡＩ連携機能の自己テストを開始します。', 'wait':0, })
        speech_run(runMode, speechs, lang, )
        speechs = []
        speechs.append({'text':u'外部ＡＩ連携機能', 'wait':0, })
        speechs.append({'text':u'スマートスピーカー等の外部機器との連携機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'それでは、外部ＡＩ連携機能の自己テストを開始します。', 'wait':0, })
        speech_run(runMode, speechs, ''  , )

        speech_wait(idolsec=5,maxwait=30, )

        speechtext  = u'ja,hoya,調子はどうですか？'

        smart = 'siri'
        smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        smtspk.wait()
        smtspk.terminate()
        smtspk = None

        speech_wait(idolsec=5,maxwait=30, )

    if (check == 'all') or (check == u'連携'):

        speechtext  = u'ja,hoya,調子はどうですか？'

        smart = 'clova'
        smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        smtspk.wait()
        smtspk.terminate()
        smtspk = None

        speech_wait(idolsec=5,maxwait=30, )

        smart = 'google'
        smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        smtspk.wait()
        smtspk.terminate()
        smtspk = None

        speech_wait(idolsec=5,maxwait=30, )

        smart = 'alexa'
        smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        smtspk.wait()
        smtspk.terminate()
        smtspk = None

        speech_wait(idolsec=5,maxwait=30, )

    if (check == 'all') or (check == u'連携') or (check == 'demo'):
        speechs = []
        speechs.append({'text':u'連携機能の紹介を終わります。', 'wait':0, })
        speech_run(runMode, speechs, lang, )
        speech_run(runMode, speechs, ''  , )



    if (check == 'all') or (check == 'demo'):
        speech_wait(idolsec=5,maxwait=30, )

        speechs = []
        speechs.append({'text':u'自己診断と機能紹介が終わりました。', 'wait':0, })
        speechs.append({'text':u'いかがでしたでしょうか。ありがとうございました', 'wait':0, })
        speech_run(runMode, speechs, lang, )
        speech_run(runMode, speechs, ''  , )



    qLogOutput('')
    qLogOutput('self_check:terminate')

    qLogOutput('self_check:bye!')


