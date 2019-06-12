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

import platform
qOS = platform.system().lower() #windows,darwin,linux

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)



qApiInp    = 'free'
qApiTrn    = 'free'
qApiOut    = 'free'
if (qOS == 'windows'):
    qApiOut = 'winos'
if (qOS == 'darwin'):
    qApiOut = 'macos'
qLangInp   = 'ja'
qLangTrn   = 'en,fr,'
qLangTxt   = qLangInp
qLangOut   = qLangTrn[:2]

qPathCtrl  = 'temp/a3_0control/'
qPathSTT   = 'temp/a3_3stt_txt/'
qPathTTS   = 'temp/a3_5tts_txt/'
qPathTRA   = 'temp/a3_6tra_txt/'
qPathRec   = 'temp/a3_8recorder/'
qPathWork  = 'temp/a3_9work/'

qCtrlRecognize = 'temp/temp_recognize.txt'
qCtrlTranslate = 'temp/temp_translate.txt'



# google 音声認識、翻訳機能、音声合成
import speech_api_google     as google_api
import speech_api_google_key as google_key

# watson 音声認識、翻訳機能、音声合成
import speech_api_watson     as watson_api
import speech_api_watson_key as watson_key

# azure 音声認識、翻訳機能、音声合成
import speech_api_azure     as azure_api
import speech_api_azure_key as azure_key

# nict 音声認識,翻訳機能,音声合成
import speech_api_nict     as nict_api
import speech_api_nict_key as nict_key

# docomo 音声認識
import speech_api_docomo     as docomo_api
import speech_api_docomo_key as docomo_key

# hoya 音声合成
import speech_api_hoya     as hoya_api
import speech_api_hoya_key as hoya_key

# winos 音声合成
if (qOS == 'windows'):
    import speech_api_winos as winos_api

# macos 音声合成
if (qOS == 'darwin'):
    import speech_api_macos as macos_api



def qVoiceInput(useApi='free', inpLang='auto', inpFile='_sound_hallo.wav', apiRecovery=True, ):
    resText = ''
    resApi  = ''

    api   = useApi
    if  (api != 'free') and (api != 'google') and (api != 'google8k') \
    and (api != 'watson') and (api != 'azure') \
    and (api != 'docomo') and (api != 'nict'):
        api = 'free'

    if (resText == '') and (api == 'watson'):
        watsonAPI = watson_api.SpeechAPI()
        res = watsonAPI.authenticate('stt',
                   watson_key.getkey('stt','username'),
                   watson_key.getkey('stt','password'), )
        if (res == True):
            resText, resApi = watsonAPI.recognize(inpWave=inpFile, inpLang=inpLang)
        if (resText == '') and (apiRecovery == True):
            api   = 'free'

    if (resText == '') and (api == 'azure'):
        azureAPI = azure_api.SpeechAPI()
        ver, key = azure_key.getkey('stt')
        res = azureAPI.authenticate('stt', ver, key, )
        if (res == True):
            resText, resApi = azureAPI.recognize(inpWave=inpFile, inpLang=inpLang)
        if (resText == '') and (apiRecovery == True):
            api   = 'free'

    if (resText == '') and (api == 'nict'):
        nictAPI = nict_api.SpeechAPI()
        res = nictAPI.authenticate('stt',
                   nict_key.getkey('stt', 'id' ),
                   nict_key.getkey('stt', 'key'), )
        if (res == True):
            resText, resApi = nictAPI.recognize(inpWave=inpFile, inpLang=inpLang, api='auto')
        if (resText == '') and (apiRecovery == True):
            api   = 'free'

    if (resText == '') and (api == 'docomo'):
        docomoAPI = docomo_api.SpeechAPI()
        res = docomoAPI.authenticate('stt', docomo_key.getkey('stt'), )
        if (res == True):
            resText, resApi = docomoAPI.recognize(inpWave=inpFile, inpLang=inpLang)
        if (resText == '') and (apiRecovery == True):
            api   = 'free'

    if (resText == '') and (api == 'google' or api == 'google8k' or api == 'free'):
        googleAPI = google_api.SpeechAPI()
        res = googleAPI.authenticate('stt', google_key.getkey('stt'), )
        if (res == True):
            if   (api == 'google'):
                resText, resApi = googleAPI.recognize(inpWave=inpFile, inpLang=inpLang, api=api)
            elif (api == 'google8k'):
                resText, resApi = googleAPI.recognize(inpWave=inpFile, inpLang=inpLang, api=api)
            else:
                resText, resApi = googleAPI.recognize(inpWave=inpFile, inpLang=inpLang, api=api)

    if (resText != ''):
        return resText, resApi

    return '', ''



def qTranslator_cacheFile(useApi='free', inpLang='ja', outLang='en', inpText=u'こんにちわ', ):
    if (inpText != '') and (inpText != '!'):
        f = inpText.replace(' ','_')
        f = f.replace(u'　','_')
        f = f.replace(u'、','_')
        f = f.replace(u'。','_')
        f = f.replace('"','_')
        f = f.replace('$','_')
        f = f.replace('%','_')
        f = f.replace('&','_')
        f = f.replace("'",'_')
        f = f.replace('\\','_')
        f = f.replace('|','_')
        f = f.replace('*','_')
        f = f.replace('/','_')
        f = f.replace('?','_')
        f = f.replace(':',',')
        f = f.replace('<','_')
        f = f.replace('>','_')
        if (inpLang == 'ja'):
            f = f.replace('_','')
        while (f[:1] == '_'):
            f = f[1:]
        while (f[-1:] == '_'):
            f = f[:-1]

        cacheFile='temp/_cache/' + f + '_' + inpLang + '_' + outLang + '_' + useApi + '_utf8.txt'
        return cacheFile

    return ''

def qTranslator_fromCache(useApi='free', inpLang='ja', outLang='en', inpText=u'こんにちわ', ):
    cacheFile = qTranslator_cacheFile(useApi=useApi, inpLang=inpLang, outLang=outLang, inpText=inpText, )
    if (cacheFile != ''):
        if (os.path.exists(cacheFile)):
            try:
                txt = ''
                rt = codecs.open(cacheFile, 'r', 'utf-8')
                for t in rt:
                    txt = (txt + ' ' + str(t)).strip()
                rt.close
                rt = None

                if (txt != '' and txt != '!'):
                    return True, txt
            except:
                pass

    return False, ''

def qTranslator_toCache(useApi='free', inpLang='ja', outLang='en', inpText=u'こんにちわ', outText='Hello', ):
    cacheFile = qTranslator_cacheFile(useApi=useApi, inpLang=inpLang, outLang=outLang, inpText=inpText, )
    if (cacheFile == ''):
        return False
    if (os.path.exists(cacheFile)):
        return True
    if (len(cacheFile) > 128):
        return False
    if (inpLang != 'ja') and (inpLang != 'en'):
        return False
    #if (outLang != 'ja') and (outLang != 'en'):
    #    return False
    if (outText == '') or (outText == '!'):
        return False

    try:
        w = codecs.open(cacheFile, 'w', 'utf-8')
        w.write(outText)
        w.close()
        w = None
        return True
    except:
        w = None

    return False



def qTranslator(useApi='free', inpLang='ja', outLang='en', inpText=u'こんにちわ', apiRecovery=True, ):
    resText = ''
    resApi  = ''

    api = useApi
    if  (api != 'free') and (api != 'google') \
    and (api != 'watson') and (api != 'azure') \
    and (api != 'nict'):
        api = 'free'
    if (inpText == '' or inpLang == outLang):
        api = 'none'

    apirun = True

    if (apirun == True):

        if (resText == ''):
            res, txt = qTranslator_fromCache(useApi=api, inpLang=inpLang, outLang=outLang, inpText=inpText, )
            if (res == True):
                resText = txt
                resApi  = api
                apirun  = False
            if (resText == '') and (useApi == 'google'):
                res, txt = qTranslator_fromCache(useApi='free', inpLang=inpLang, outLang=outLang, inpText=inpText, )
                if (res == True):
                    resText = txt
                    resApi  = 'free'
                    apirun  = False
            if (resText == '') and (useApi == 'free'):
                res, txt = qTranslator_fromCache(useApi='google', inpLang=inpLang, outLang=outLang, inpText=inpText, )
                if (res == True):
                    resText = txt
                    resApi  = 'google'
                    apirun  = False

        if (resText == '') and (api == 'none'):
            resText = inpText
            resApi  = api
            apirun  = False

        if (resText == '') and (api == 'watson'):
            watsonAPI = watson_api.SpeechAPI()
            res = watsonAPI.authenticate('tra',
                       watson_key.getkey('tra','username'),
                       watson_key.getkey('tra','password'), )
            if (res == True):
                if (inpLang == 'en' or outLang == 'en'):
                    resText , resApi = watsonAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, )
                else:
                    resTextx, resApi = watsonAPI.translate(inpText=inpText,  inpLang=inpLang, outLang='en', )
                    resText , resApi = watsonAPI.translate(inpText=resTextx, inpLang='en', outLang=outLang, )
            if (resText == '') and (apiRecovery == True):
                api = 'free'

        if (resText == '') and (api == 'azure'):
            azureAPI = azure_api.SpeechAPI()
            ver, key = azure_key.getkey('tra')
            res = azureAPI.authenticate('tra', ver, key, )
            if (res == True):
                resText, resApi = azureAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, )
            if (resText == '') and (apiRecovery == True):
                api = 'free'

        if (resText == '') and (api == 'nict'):
            nictAPI = nict_api.SpeechAPI()
            res = nictAPI.authenticate('tra',
                       nict_key.getkey('tra', 'id' ),
                       nict_key.getkey('tra', 'key'), )
            if (res == True):
                resText, resApi = nictAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, )
            if (resText == '') and (apiRecovery == True):
                api = 'free'

        if (resText == '') and (api == 'free') and (useApi != 'free'):
            res, txt = qTranslator_fromCache(useApi=api, inpLang=inpLang, outLang=outLang, inpText=inpText, )
            if (res == True):
                resText = txt
                resApi  = api
                apirun  = False

        if (resText == '') and (api == 'google' or api == 'free'):
            googleAPI = google_api.SpeechAPI()
            res = googleAPI.authenticate('tra', google_key.getkey('tra'), )
            if (res == True):
                if   (api == 'google'):
                    resText, resApi = googleAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, api=api, )
                else:
                    resText, resApi = googleAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, api=api, )

    if (apirun == True):
        if (resText != ''):
            qTranslator_toCache(useApi=resApi, inpLang=inpLang, outLang=outLang, inpText=inpText, outText=resText, )

    if (resText != ''):
        return resText, resApi

    return '', ''



def qVoiceOutput_cacheFile(useApi='free', outLang='en', outText='Hallo', ):
    if (outText != '') and (outText != '!'):
        f = outText.replace(' ','_')
        f = f.replace(u'　','_')
        f = f.replace(u'、','_')
        f = f.replace(u'。','_')
        f = f.replace('"','_')
        f = f.replace('$','_')
        f = f.replace('%','_')
        f = f.replace('&','_')
        f = f.replace("'",'_')
        f = f.replace('\\','_')
        f = f.replace('|','_')
        f = f.replace('*','_')
        f = f.replace('/','_')
        f = f.replace('?','_')
        f = f.replace(':',',')
        f = f.replace('<','_')
        f = f.replace('>','_')
        if (outLang == 'ja'):
            f = f.replace('_','')
        while (f[:1] == '_'):
            f = f[1:]
        while (f[-1:] == '_'):
            f = f[:-1]

        cacheFile='temp/_cache/' + f + '_' + outLang + '_' + useApi + '.mp3'
        return cacheFile

    return ''

def qVoiceOutput_fromCache(useApi='free', outLang='en', outText='Hallo', outFile='temp/temp_Hallo.mp3',):
    cacheFile = qVoiceOutput_cacheFile(useApi=useApi, outLang=outLang, outText=outText, )
    if (cacheFile != ''):
        if (os.path.exists(cacheFile)):
            try:
                if (cacheFile[-4:].lower() == outFile[-4:].lower()):
                    shutil.copy2(cacheFile, outFile)
                    return True
                else:
                    sox = subprocess.Popen(['sox', '-q', cacheFile, outFile, ], \
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    sox.wait()
                    sox.terminate()
                    sox = None
                    return True
            except:
                pass
    return False

def qVoiceOutput_toCache(useApi='free', outLang='en', outText='Hallo', tempFile=''):
    cacheFile = qVoiceOutput_cacheFile(useApi=useApi, outLang=outLang, outText=outText, )
    if (cacheFile == ''):
        return False
    if (os.path.exists(cacheFile)):
        return True
    if (len(cacheFile) > 128):
        return False
    if (outLang != 'ja') and (outLang != 'en'):
        return False
    if (outText == '') or (outText == '!'):
        return False
    if (not os.path.exists(tempFile)):
        return False

    try:
        if (tempFile[-4:].lower() == cacheFile[-4:].lower()):
            shutil.copy2(tempFile, cacheFile)
            return True
        else:
            sox = subprocess.Popen(['sox', '-q', tempFile, cacheFile, ], \
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox.wait()
            sox.terminate()
            sox = None
            return True
    except:
        pass

    return False

def qVoiceOutput(useApi='free', outLang='en', outText='Hallo', outFile='temp/temp_Hallo.mp3', tempFile='', apiRecovery=True, ):
    resText = ''
    resApi  = ''

    if (os.path.exists(outFile)):
        try:
            os.remove(outFile)
        except:
            pass

    if (tempFile == ''):
        tempFileWav='temp/temp_qVoiceOutput.wav'
        tempFileMp3='temp/temp_qVoiceOutput.mp3'
    else:
        tempFileWav=tempFile[:-4] + '.wav'
        tempFileMp3=tempFile[:-4] + '.mp3'
    if (os.path.exists(tempFileWav)):
        try:
            os.remove(tempFileWav)
        except:
            pass
    if (os.path.exists(tempFileMp3)):
        try:
            os.remove(tempFileMp3)
        except:
            pass

    api   = useApi
    if  (api != 'free')   and (api != 'google') \
    and (api != 'watson') and (api != 'azure') \
    and (api != 'winos')  and (api != 'macos') \
    and (api != 'hoya')  and (api != 'nict'):
        api = 'free'

    apirun = True

    if (apirun == True):

        if (resText == ''):
            res = qVoiceOutput_fromCache(useApi=api, outLang=outLang, outText=outText, outFile=outFile,)
            if (res == True):
                resText = outText
                resApi  = api
                apirun  = False
            if (resText == '') and (useApi == 'google'):
                res = qVoiceOutput_fromCache(useApi='free', outLang=outLang, outText=outText, outFile=outFile,)
                if (res == True):
                    resText = outText
                    resApi  = 'free'
                    apirun  = False
            if (resText == '') and (useApi == 'free'):
                res = qVoiceOutput_fromCache(useApi='google', outLang=outLang, outText=outText, outFile=outFile,)
                if (res == True):
                    resText = outText
                    resApi  = 'google'
                    apirun  = False

        if (resText == '') and (api == 'watson'):
            watsonAPI = watson_api.SpeechAPI()
            res = watsonAPI.authenticate('tts',
                       watson_key.getkey('tts','username'),
                       watson_key.getkey('tts','password'), )
            if (res == True):
                resText, resApi = watsonAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, )
                if (resText != ''):
                    if (tempFileMp3[-4:].lower() == outFile[-4:].lower()):
                        shutil.copy2(tempFileMp3, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileMp3, outFile, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'azure'):
            azureAPI = azure_api.SpeechAPI()
            ver, key = azure_key.getkey('tts')
            res = azureAPI.authenticate('tts', ver, key, )
            if (res == True):
                resText, resApi = azureAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, )
                if (resText != ''):
                    if (tempFileMp3[-4:].lower() == outFile[-4:].lower()):
                        shutil.copy2(tempFileMp3, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileMp3, outFile, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'winos'):
            winosAPI = winos_api.SpeechAPI()
            res = winosAPI.authenticate()
            if (res == True):
                resText, resApi = winosAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                if (resText != ''):
                    if (tempFileWav[-4:].lower() == outFile[-4:].lower()):
                        shutil.copy2(tempFileWav, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileWav, outFile, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'macos'):
            macosAPI = macos_api.SpeechAPI()
            res = macosAPI.authenticate()
            if (res == True):
                resText, resApi = macosAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                if (resText != ''):
                    if (tempFileWav[-4:].lower() == outFile[-4:].lower()):
                        shutil.copy2(tempFileWav, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileWav, outFile, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'nict'):
            nictAPI = nict_api.SpeechAPI()
            res = nictAPI.authenticate('tts',
                       nict_key.getkey('tts', 'id' ),
                       nict_key.getkey('tts', 'key'), )
            if (res == True):
                resText, resApi = nictAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                if (resText != ''):
                    if (tempFileWav[-4:].lower() == outFile[-4:].lower()):
                        shutil.copy2(tempFileWav, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileWav, outFile, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'hoya'):
            hoyaAPI = hoya_api.SpeechAPI()
            res = hoyaAPI.authenticate(hoya_key.getkey(), )
            if (res == True):
                resText, resApi = hoyaAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                if (resText != ''):
                    if (tempFileWav[-4:].lower() == outFile[-4:].lower()):
                        shutil.copy2(tempFileWav, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileWav, outFile, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'free') and (useApi != 'free'):
            res = qVoiceOutput_fromCache(useApi=api, outLang=outLang, outText=outText, outFile=outFile,)
            if (res == True):
                resText = outText
                resApi  = api
                apirun  = False

        if (resText == '') and (api == 'google' or api == 'free'):
            googleAPI = google_api.SpeechAPI()
            res = googleAPI.authenticate('tts', google_key.getkey('tts'), )
            if (res == True):
                if (api == 'google'):
                    resText, resApi = googleAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, api='auto', )
                else:
                    resText, resApi = googleAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, api='free', )
                if (resText != ''):
                    if (tempFileMp3[-4:].lower() == outFile[-4:].lower()):
                        shutil.copy2(tempFileMp3, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileMp3, outFile, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None

    if (apirun == True):
        if (resText != ''):
            if (resApi == 'google' or resApi == 'free' or resApi == 'watson'):
                qVoiceOutput_toCache(useApi=resApi, outLang=outLang, outText=resText, tempFile=tempFileMp3,)
            else:
                qVoiceOutput_toCache(useApi=resApi, outLang=outLang, outText=resText, tempFile=tempFileWav,)

    try:
        if (os.path.exists(tempFileWav)):
            os.remove(tempFileWav)
        if (os.path.exists(tempFileMp3)):
            os.remove(tempFileMp3)
    except:
        pass

    if (resText != ''):
        return resText, resApi

    return '', ''



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
def qLogOutput(pLogText='', pDisplay=False, pOutfile=True):
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
    qMakeDirs('temp/_log/',   False)
    qMakeDirs('temp/_cache/', False)

    qLogOutput('___main___:init')

    qLogOutput('___main___:exsample.py runMode, api..., lang..., ')
    #runMode  handsfree, translator, speech, ...,
    #api      free, google, watson, azure, nict, winos, macos, docomo,
    #lang     ja, en, fr, kr...

    runMode  = 'debug'
    micDev   = '0'

    procId   = '00'
    fileId   = 'temp_sample'

    inpInput = '_sound_hallo.wav'
    inpOutput= 'temp/temp_sample_ja.txt'
    trnInput = 'temp/temp_sample_ja.txt'
    trnOutput= 'temp/temp_sample_en.txt'
    txtInput = 'temp/temp_sample_ja.txt'
    txtOutput= 'temp/temp_sample_ja.mp3'
    outInput = 'temp/temp_sample_en.txt'
    outOutput= 'temp/temp_sample_en.mp3'

    inpPlay  = 'on'
    txtPlay  = 'off'
    outPlay  = 'on'

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        micDev   = str(sys.argv[2]).lower()
    if (len(sys.argv) >= 4):
        qApiInp  = str(sys.argv[3]).lower()
        if (qApiInp == 'google') or (qApiInp == 'watson') \
        or (qApiInp == 'azure')  or (qApiInp == 'nict'):
            qApiTrn  = qApiInp
            qApiOut  = qApiInp
        else:
            qApiTrn  = 'free'
            qApiOut  = 'free'
    if (len(sys.argv) >= 5):
        qApiTrn  = str(sys.argv[4]).lower()
    if (len(sys.argv) >= 6):
        qApiOut  = str(sys.argv[5]).lower()
    if (len(sys.argv) >= 7):
        qLangInp = str(sys.argv[6]).lower()
        qLangTxt = qLangInp
    if (len(sys.argv) >= 8):
        qLangTrn = str(sys.argv[7]).lower()
        qLangOut = qLangTrn[:2]
    if (len(sys.argv) >= 9):
        qLangTxt = str(sys.argv[8]).lower()
    if (len(sys.argv) >= 10):
        qLangOut = str(sys.argv[9]).lower()

    if (len(sys.argv) >= 11):
        procId   = sys.argv[10]
    if (len(sys.argv) >= 12):
        fileId   = sys.argv[11]

    if (len(sys.argv) >= 13):
        inpInput = sys.argv[12]
    if (len(sys.argv) >= 14):
        inpOutput= sys.argv[13]
    if (len(sys.argv) >= 15):
        trnInput = sys.argv[14]
    if (len(sys.argv) >= 16):
        trnOutput= sys.argv[15]
    if (len(sys.argv) >= 17):
        txtInput = sys.argv[16]
    if (len(sys.argv) >= 18):
        txtOutput= sys.argv[17]
    if (len(sys.argv) >= 19):
        outInput = sys.argv[18]
    if (len(sys.argv) >= 20):
        outOutput= sys.argv[19]

    if (len(sys.argv) >= 21):
        inpPlay  = str(sys.argv[20]).lower()
    if (len(sys.argv) >= 22):
        txtPlay  = str(sys.argv[21]).lower()
    if (len(sys.argv) >= 23):
        outPlay  = str(sys.argv[22]).lower()

    qLogOutput('')
    qLogOutput('___main___:runMode  =' + str(runMode  ))
    qLogOutput('___main___:micDev   =' + str(micDev   ))
    qLogOutput('___main___:qApiInp  =' + str(qApiInp  ))
    qLogOutput('___main___:qApiTrn  =' + str(qApiTrn  ))
    qLogOutput('___main___:qApiOut  =' + str(qApiOut  ))
    qLogOutput('___main___:qLangInp =' + str(qLangInp ))
    qLogOutput('___main___:qLangTrn =' + str(qLangTrn ))
    qLogOutput('___main___:qLangTxt =' + str(qLangTxt ))
    qLogOutput('___main___:qLangOut =' + str(qLangOut ))

    qLogOutput('___main___:procId   =' + str(procId   ))
    qLogOutput('___main___:fileId   =' + str(fileId   ))

    qLogOutput('___main___:inpInput =' + str(inpInput ))
    qLogOutput('___main___:inpOutput=' + str(inpOutput))
    qLogOutput('___main___:trnInput =' + str(trnInput ))
    qLogOutput('___main___:trnOutput=' + str(trnOutput))
    qLogOutput('___main___:txtInput =' + str(txtInput ))
    qLogOutput('___main___:txtOutput=' + str(txtOutput))
    qLogOutput('___main___:outInput =' + str(outInput ))
    qLogOutput('___main___:outOutput=' + str(outOutput))

    qLogOutput('___main___:inpPlay  =' + str(inpPlay  ))
    qLogOutput('___main___:txtPlay  =' + str(txtPlay  ))
    qLogOutput('___main___:outPlay  =' + str(outPlay  ))



    qLogOutput('')
    qLogOutput('___main___:start')

    inpRun  = False
    inpText = ''
    txtRun  = False
    txtText = ''
    txtWork = ''
    trnRun  = False
    trnIn   = ''
    trnText = ''
    outRun  = False



    if (inpInput != '' and os.path.exists(inpInput)):
        now = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d')
        recfile = qPathRec + fileId + '.stt.mp3'

        inpRun   = True
        inpText  = ''
        soxMsg1  = ''
        soxMsg2  = ''
        soxMsg3  = ''

        wrkApi   = 'free'
        if (qApiInp == 'google'):
            wrkApi = 'google8k'

        wrkfile    = ''
        wrkfile_0  = qPathWork + fileId + '_input_0.wav'
        wrkfile_0s = qPathWork + fileId + '_input_0s.wav'
        wrkfile_1  = qPathWork + fileId + '_input_1.wav'
        wrkfile_1s = qPathWork + fileId + '_input_1s.wav'
        wrkfile_2  = qPathWork + fileId + '_input_2.wav'
        wrkfile_2s = qPathWork + fileId + '_input_2s.wav'
        wrkfile_x1 = qPathWork + fileId + '_input_x1.wav'
        wrkfile_x2 = qPathWork + fileId + '_input_x2.wav'
        wrkfile_y1 = qPathWork + fileId + '_input_y1.wav'
        wrkfile_y2 = qPathWork + fileId + '_input_y2.wav'
        wrkfile_y3 = qPathWork + fileId + '_input_y3.wav'
        wrkfile_y4 = qPathWork + fileId + '_input_y4.wav'
        wrkfile_y5 = qPathWork + fileId + '_input_y5.wav'
        wrkfile_y6 = qPathWork + fileId + '_input_y6.wav'

        sox_0  = subprocess.Popen(['sox', '-q', inpInput, wrkfile_0, ], \
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        sox_0s = subprocess.Popen(['sox', '-q', inpInput, wrkfile_0s, \
                 'silence', '1', '0.5', '0.2%', '1', '0.5', '0%', ':restart', ], \
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        sox_1  = subprocess.Popen(['sox', '-q', inpInput, wrkfile_1,  '--norm', ], \
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        sox_1s = subprocess.Popen(['sox', '-q', inpInput, wrkfile_1s, '--norm', \
                 'silence', '1', '0.5', '0.2%', '1', '0.5', '0%', ':restart', ], \
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        sox_2  = subprocess.Popen(['sox', '-q', inpInput, wrkfile_2,  'gain', '+12', ], \
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        sox_2s = subprocess.Popen(['sox', '-q', inpInput, wrkfile_2s, 'gain', '+12', \
                 'silence', '1', '0.5', '0.2%', '1', '0.5', '0.1%', ':restart', ], \
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        sox_0.wait()
        sox_0.terminate()
        sox_0 = None
        if (os.path.exists(wrkfile_0)):
            inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_0, False, )
            if (runMode == 'debug'):
                qLogOutput('Debug [' + inpText + '](' + wrkApi + ') step1 normal wav ', True)

            if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                inpText = inpTextX
                soxMsg1 = ''
                wrkfile  = wrkfile_0

        sox_0s.wait()
        sox_0s.terminate()
        sox_0s = None
        if (os.path.exists(wrkfile_0s)):
            #if (str(micDev) == 'file') or (runMode == 'debug') \
            #or (inpText == '') or (inpText == '!'):
            if (str(micDev) == 'file') or (runMode == 'debug'):
                inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_0s, False, )
                if (runMode == 'debug'):
                    qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step1 sox silence 0.5s 0%', True)

                if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                    inpText = inpTextX
                    soxMsg1 = '< silence 0.5s 0% '
                    wrkfile  = wrkfile_0s

        sox_1.wait()
        sox_1.terminate()
        sox_1 = None
        if (os.path.exists(wrkfile_1)):
            #if (str(micDev) == 'file') or (runMode == 'debug') \
            #or (inpText == '') or (inpText == '!'):
            if (str(micDev) == 'file') or (runMode == 'debug'):
                inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_1, False, )
                if (runMode == 'debug'):
                    qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step1 --norm', True)

                if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                    inpText = inpTextX
                    soxMsg1 = '< --norm '
                    wrkfile  = wrkfile_1

        sox_1s.wait()
        sox_1s.terminate()
        sox_1s = None
        if (os.path.exists(wrkfile_1s)):
            if (str(micDev) == 'file') or (runMode == 'debug') \
            or (inpText == '') or (inpText == '!'):
                inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_1s, False, )
                if (runMode == 'debug'):
                    qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step1 --norm silence 0.5s 0%', True)

                if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                    inpText = inpTextX
                    soxMsg1 = '< --norm silence 0.5s 0% '
                    wrkfile  = wrkfile_1s

        sox_2.wait()
        sox_2.terminate()
        sox_2 = None
        if (os.path.exists(wrkfile_2)):
            #if (str(micDev) == 'file') or (runMode == 'debug') \
            #or (inpText == '') or (inpText == '!'):
            if (str(micDev) == 'file') or (runMode == 'debug'):
                inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_2, False, )
                if (runMode == 'debug'):
                    qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step1 gain +12', True)

                if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                    inpText = inpTextX
                    soxMsg1 = '< gain +12 '
                    wrkfile  = wrkfile_2

        sox_2s.wait()
        sox_2s.terminate()
        sox_2s = None
        if (os.path.exists(wrkfile_2s)):
            #if (str(micDev) == 'file') or (runMode == 'debug') \
            #or (inpText == '') or (inpText == '!'):
            if (str(micDev) == 'file') or (runMode == 'debug'):
                inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_2s, False, )
                if (runMode == 'debug'):
                    qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step1 gain +12 silence 0.5s 0.1%', True)

                if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                    inpText = inpTextX
                    soxMsg1 = '< gain +12 silence 0.5s 0.1% '
                    wrkfile  = wrkfile_2s

        if (wrkfile == ''):
            wrkfile  = wrkfile_0

        if (os.path.exists(wrkfile)):
            if (str(micDev) == 'file') or (runMode == 'debug'):

                sox_x1 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_x1, \
                         'silence', '1', '0.3', '0.5%', '1', '0.3', '0.5%', ':restart', ], \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox_x2 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_x2, \
                         'silence', '1', '0.3', '1%', '1', '0.3', '1%', ':restart', ], \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                sox_x1.wait()
                sox_x1.terminate()
                sox_x1 = None
                if (os.path.exists(wrkfile_x1)):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_x1, False, )
                    if (runMode == 'debug'):
                        qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step2 silence 0.3s 0.5%', True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg2 = '< silence 0.3s 0.5% '
                        wrkfile  = wrkfile_x1

                sox_x2.wait()
                sox_x2.terminate()
                sox_x2 = None
                if (os.path.exists(wrkfile_x2)):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_x2, False, )
                    if (runMode == 'debug'):
                        qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step2 silence 0.3s 1.0%', True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg2 = '< silence 0.3s 1.0% '
                        wrkfile  = wrkfile_x2

        if (os.path.exists(wrkfile)):
            if (str(micDev) == 'file') or (runMode == 'debug'):

                sox_y1 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y1, \
                         'highpass', '50', ], \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox_y2 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y2, \
                         'equalizer', '500', '1.0q', '3', ], \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox_y3 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y3, \
                         'highpass', '50', 'equalizer', '500', '1.0q', '3', ], \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox_y4 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y4, \
                         'treble', '+2', ], \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox_y5 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y5, \
                         'highpass', '50', 'treble', '+2', ], \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox_y6 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y6, \
                         'highpass', '50', 'equalizer', '500', '1.0q', '3', 'treble', '+2', ], \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                sox_y1.wait()
                sox_y1.terminate()
                sox_y1 = None
                if (os.path.exists(wrkfile_y1)):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y1, False, )
                    if (runMode == 'debug'):
                        qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step3 highpass 50', True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg3 = '< highpass 50 '
                        wrkfile  = wrkfile_y1

                sox_y2.wait()
                sox_y2.terminate()
                sox_y2 = None
                if (os.path.exists(wrkfile_y2)):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y2, False, )
                    if (runMode == 'debug'):
                        qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step3 equalizer 500 1.0q 3', True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg3 = '< equalizer 500 1.0q 3 '
                        wrkfile  = wrkfile_y2

                sox_y3.wait()
                sox_y3.terminate()
                sox_y3 = None
                if (os.path.exists(wrkfile_y3)):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y3, False, )
                    if (runMode == 'debug'):
                        qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step3 highpass + equalizer', True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg3 = '< highpass + equalizer '
                        wrkfile  = wrkfile_y3

                sox_y4.wait()
                sox_y4.terminate()
                sox_y4 = None
                if (os.path.exists(wrkfile_y4)):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y4, False, )
                    if (runMode == 'debug'):
                        qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step3 treble +2', True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg3 = '< treble +2 '
                        wrkfile  = wrkfile_y4

                sox_y5.wait()
                sox_y5.terminate()
                sox_y5 = None
                if (os.path.exists(wrkfile_y5)):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y5, False, )
                    if (runMode == 'debug'):
                        qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step3 highpass + treble', True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg3 = '< highpass + treble '
                        wrkfile  = wrkfile_y5

                sox_y6.wait()
                sox_y6.terminate()
                sox_y6 = None
                if (os.path.exists(wrkfile_y6)):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y6, False, )
                    if (runMode == 'debug'):
                        qLogOutput('Debug [' + inpTextX + '](' + wrkApi + ') step3 highpass + equalizer + treble', True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg3 = '< highpass + equalizer + treble '
                        wrkfile  = wrkfile_y6

        if (wrkfile[-4:].lower() == recfile[-4:].lower()):
            shutil.copy2(wrkfile, recfile)
        else:
            sox = subprocess.Popen(['sox', '-q', wrkfile, recfile, ], \
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox.wait()
            sox.terminate()
            sox = None

        if (inpPlay == 'on' or inpPlay == 'yes'):
            sox = subprocess.Popen(['sox', '-q', recfile, '-d', '--norm', ], \
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox.wait()
            sox.terminate()
            sox = None

        if  ((wrkApi == 'free') or (wrkApi == 'google8k')) \
        and ((qApiInp != 'free') and (qApiInp != 'google')) \
        or  ((wrkApi != 'free') or (wrkApi != 'google8k')) and (qApiInp != wrkApi):
            if (os.path.exists(wrkfile)):

                #inpTextX,api = qVoiceInput(qApiInp, qLangInp, wrkfile, False, )
                inpTextX,api = qVoiceInput(qApiInp, qLangInp, wrkfile, )
                if (inpTextX != '' and inpTextX != '!'):
                    inpText = inpTextX
                else:
                    api = wrkApi

        if (os.path.exists(wrkfile_0)):
            os.remove(wrkfile_0)
        if (os.path.exists(wrkfile_0s)):
            os.remove(wrkfile_0s)
        if (os.path.exists(wrkfile_1)):
            os.remove(wrkfile_1)
        if (os.path.exists(wrkfile_1s)):
            os.remove(wrkfile_1s)
        if (os.path.exists(wrkfile_2)):
            os.remove(wrkfile_2)
        if (os.path.exists(wrkfile_2s)):
            os.remove(wrkfile_2s)
        if (os.path.exists(wrkfile_x1)):
            os.remove(wrkfile_x1)
        if (os.path.exists(wrkfile_x2)):
            os.remove(wrkfile_x2)
        if (os.path.exists(wrkfile_y1)):
            os.remove(wrkfile_y1)
        if (os.path.exists(wrkfile_y2)):
            os.remove(wrkfile_y2)
        if (os.path.exists(wrkfile_y3)):
            os.remove(wrkfile_y3)
        if (os.path.exists(wrkfile_y4)):
            os.remove(wrkfile_y4)
        if (os.path.exists(wrkfile_y5)):
            os.remove(wrkfile_y5)
        if (os.path.exists(wrkfile_y6)):
            os.remove(wrkfile_y6)

        if (inpText != '' and inpText != '!') and (soxMsg1 != '' or soxMsg2 != '' or soxMsg3 != ''):
            qLogOutput(' ' + procId + ' Recognition  <<<<' + soxMsg3 + soxMsg2 + soxMsg1 + '<<<<< wav', True)

        if (inpText == ''):
            inpText = '!'

        if (api == qApiInp) or (api == 'free' and qApiInp == 'google'):
                qLogOutput(' ' + procId + ' Recognition  [' + inpText + '] ' + qLangInp + ' (' + api + ')', True)
        else:
            if (api != ''):
                qLogOutput(' ' + procId + ' Recognition  [' + inpText + '] ' + qLangInp + ' (!' + api + ')', True)
            else:
                qLogOutput(' ' + procId + ' Recognition  [' + inpText + '] ' + qLangInp + ' (!' + qApiInp + ')', True)

        if (inpText != '' and inpText != '!') and (runMode == 'number'):
            numtxt = inpText
            numtxt = numtxt.replace(u'ゼロ', '0')
            numtxt = numtxt.replace(u'０',   '0')
            numtxt = numtxt.replace(u'１',   '1')
            numtxt = numtxt.replace(u'２',   '2')
            numtxt = numtxt.replace(u'３',   '3')
            numtxt = numtxt.replace(u'４',   '4')
            numtxt = numtxt.replace(u'５',   '5')
            numtxt = numtxt.replace(u'６',   '6')
            numtxt = numtxt.replace(u'７',   '7')
            numtxt = numtxt.replace(u'８',   '8')
            numtxt = numtxt.replace(u'９',   '9')
            numtxt = numtxt.replace(u'。', '')
            numtxt = numtxt.replace(u'．', '.')
            numtxt = numtxt.replace(u'　', '')
            numtxt = numtxt.replace(' ', '')
            numtxt = numtxt.replace(',', '')
            if (numtxt[-1:] == '.'):
                numtxt=numtxt[:-1]
            if (numtxt != inpText and numtxt.isdigit()):
                qLogOutput(' ' + procId + ' Recognition  [' + inpText + u'] → [' + numtxt + ']', True)
                inpText = str(numtxt)



    if (inpOutput != '' and inpText != ''):
        try:
            w = codecs.open(inpOutput, 'w', 'utf-8')
            w.write(inpText)
            w.close()
            w = None
        except:
            w = None

        if (True):
            if (inpText != '' and inpText != '!'):
                try:
                    w = codecs.open(qCtrlRecognize, 'w', 'utf-8')
                    w.write(qLangInp + ', [' + inpText + ']')
                    w.close()
                    w = None
                except:
                    w = None

                file = inpOutput.replace(qPathSTT, '')
                file = file.replace(qPathTRA, '')
                file = file.replace(qPathTTS, '')
                file = file.replace(qPathWork, '')
                file = qPathCtrl + file
                try:
                    w = codecs.open(file, 'w', 'utf-8')
                    w.write(inpText)
                    w.close()
                    w = None
                except:
                    w = None

        now = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d')
        recfile = qPathRec + fileId + '.stt.txt'
        recutf8 = qPathRec + '_' + stamp + '_stt_utf8.txt'
        recsjis = qPathRec + '_' + stamp + '_stt_sjis.txt'

        try:
            w = codecs.open(recfile, 'w', 'utf-8')
            w.write(inpText)
            w.close()
            w = None
        except:
            w = None

        try:
            a = codecs.open(recutf8, 'a', 'utf-8')
            a.write(fileId + ', [' + inpText + ']\n')
            a.close()
            a = None
        except:
            a = None

        try:
            a = codecs.open(recsjis, 'a', 'shift_jis')
            a.write(fileId + ', [' + inpText + ']\r\n')
            a.close()
            a = None
        except:
            a = None



    if (trnInput != ''):
        trnRun   = True
        trnIn    = ''
        trnText  = ''
        trnMulti = []

        if (trnInput == inpOutput ):
            trnIn = inpText
        else:
            try:
                rt = codecs.open(trnInput, 'r', 'utf-8')
                for t in rt:
                    trnIn = (trnIn + ' ' + str(t)).strip()
                rt.close
                rt = None
            except:
                rt = None

        while (trnIn[:3] == 'ja,' or trnIn[:3] == 'en,'):
            trnIn = trnIn[3:]

        if (trnIn == ''):
            trnIn = '!'

        if (trnIn != '!'):
            if (inpInput == ''):
                                    qLogOutput(' ' + procId + ' Text Input   [' + trnIn + '] ' + qLangInp, True)
            langs = qLangTrn.split(',')
            for lang in langs:
                lang = str(lang).strip()
                if (lang != ''):
                    trnRes,api = qTranslator(qApiTrn, qLangInp, lang, trnIn, )
                    if (trnRes != '' and trnRes != '!'):
                        if (api == qApiTrn) or (api == 'free' and qApiTrn == 'google'):
                                if (inpInput != ''):
                                    qLogOutput(' ' + procId + ' Translation  [' + trnRes + '] ' + lang + ' (' + api + ')', True)
                                else:
                                    qLogOutput(' ' + procId + ' Text Trans   [' + trnRes + '] ' + lang + ' (' + api + ')', True)
                        else:
                            if (api != ''):
                                if (inpInput != ''):
                                    qLogOutput(' ' + procId + ' Translation  [' + trnRes + '] ' + lang + ' (!' + api + ')', True)
                                else:
                                    qLogOutput(' ' + procId + ' Text Trans   [' + trnRes + '] ' + lang + ' (!' + api + ')', True)
                            else:
                                if (inpInput != ''):
                                    qLogOutput(' ' + procId + ' Translation  [' + trnRes + '] ' + lang + ' (!' + qApiTrn + ')', True)
                                else:
                                    qLogOutput(' ' + procId + ' Text Trans   [' + trnRes + '] ' + lang + ' (!' + qApiTrn + ')', True)

                    if (trnRes == ''):
                        trnRes = '!'

                    if (trnRes != '' and trnRes != '!') and (runMode == 'number'):
                        numtxt = trnRes.lower()
                        numtxt = numtxt.replace(u'０', '0')
                        numtxt = numtxt.replace('zero', '0')
                        numtxt = numtxt.replace('one', '1')
                        numtxt = numtxt.replace('two', '2')
                        numtxt = numtxt.replace('three', '3')
                        numtxt = numtxt.replace('four', '4')
                        numtxt = numtxt.replace('five', '5')
                        numtxt = numtxt.replace('six', '6')
                        numtxt = numtxt.replace('seven', '7')
                        numtxt = numtxt.replace('eight', '8')
                        numtxt = numtxt.replace('nine', '9')
                        numtxt = numtxt.replace(u'。', '')
                        numtxt = numtxt.replace(u'．', '.')
                        numtxt = numtxt.replace(u'　', '')
                        numtxt = numtxt.replace(' ', '')
                        numtxt = numtxt.replace(',', '')
                        if (numtxt[-1:] == '.'):
                            numtxt=numtxt[:-1]
                        if (numtxt != trnRes and numtxt.isdigit()):
                            qLogOutput(' ' + procId + ' Translation  [' + trnRes + u'] → [' + numtxt + ']', True)
                            trnRes = str(numtxt)

                    trnMulti.append({'lang':lang, 'text':trnRes, 'api':api,})
                    if (lang == qLangTrn[:2]):
                        trnText = trnRes



    if (trnOutput != '' and trnText != ''):

        try:
            w = codecs.open(trnOutput, 'w', 'utf-8')
            w.write(trnText)
            w.close()
            w = None
        except:
            w = None

        for trnRes in trnMulti:
            file = trnOutput
            file = file.replace('.'+qLangTrn[:2]+'.', '.'+trnRes['lang']+'.')
            if (file != trnOutput):
                try:
                    w = codecs.open(file, 'w', 'utf-8')
                    w.write(trnRes['text'])
                    w.close()
                    w = None
                except:
                    w = None

        if (True):
            if (trnText != '' and trnText != '!'):
                try:
                    w = codecs.open(qCtrlTranslate, 'w', 'utf-8')
                    for trnRes in trnMulti:
                        if (trnRes['text'] != '') and (trnRes['text'] != '!'):
                            w.write(trnRes['lang'] + ', [' + trnRes['text'] + ']\n')
                    w.close()
                    w = None
                except:
                    w = None

                for trnRes in trnMulti:
                    file = trnOutput
                    file = file.replace('.'+qLangTrn[:2]+'.', '.'+trnRes['lang']+'.')
                    if (file != trnOutput):
                        try:
                            w = codecs.open(file, 'w', 'utf-8')
                            w.write(trnRes['text'])
                            w.close()
                            w = None
                        except:
                            w = None

                file = trnOutput.replace(qPathSTT, '')
                file = file.replace(qPathTRA, '')
                file = file.replace(qPathTTS, '')
                file = file.replace(qPathWork, '')
                file = qPathCtrl + file
                try:
                    w = codecs.open(file, 'w', 'utf-8')
                    w.write(trnText)
                    w.close()
                    w = None
                except:
                    w = None

        if (inpInput != ''):
            now = datetime.datetime.now()
            stamp = now.strftime('%Y%m%d')
            recfile = qPathRec + fileId + '.translate.txt'
            recutf8 = qPathRec + '_' + stamp + '_translate_utf8.txt'
            recsjis = qPathRec + '_' + stamp + '_translate_sjis.txt'

            try:
                w = codecs.open(recfile, 'w', 'utf-8')
                w.write(trnText)
                w.close()
                w = None
            except:
                w = None

            try:
                a = codecs.open(recutf8, 'a', 'utf-8')
                a.write(fileId + ', [' + trnText + ']\n')
                a.close()
                a = None
            except:
                a = None

            try:
                a = codecs.open(recsjis, 'a', 'shift_jis')
                a.write(fileId + ', [' + trnText + ']\r\n')
                a.close()
                a = None
            except:
                a = None



    if (txtInput != ''):
        txtRun  = True
        txtText = ''
        txtInpLang = qLangTxt
        txtOutLang = qLangOut
        txtOutApi  = qApiOut

        if (txtInput == inpOutput ):
            txtText = inpText
            txtInpLang = qLangInp
            txtOutLang = qLangOut
            txtOutApi  = qApiOut
        else:
            try:
                rt = codecs.open(txtInput, 'r', 'utf-8')
                for t in rt:
                    txtText = (txtText + ' ' + str(t)).strip()
                rt.close
                rt = None
            except:
                rt = None

        while (txtText[:3] == 'ja,' or txtText[:3] == 'en,'):
            txtInpLang = txtText[:2]
            txtOutLang = txtText[:2]
            txtText = txtText[3:]

        if (txtText[:7] == 'watson,'):
            txtOutApi = txtText[:6]
            txtText = txtText[7:]
        if (txtText[:6] == 'azure,'):
            txtOutApi = txtText[:5]
            txtText = txtText[6:]
        if (txtText[:6] == 'winos,'):
            txtOutApi = txtText[:5]
            txtText = txtText[6:]
        if (txtText[:6] == 'macos,'):
            txtOutApi = txtText[:5]
            txtText = txtText[6:]
        if (txtText[:5] == 'nict,'):
            txtOutApi = txtText[:4]
            txtText = txtText[5:]
        if (txtText[:5] == 'hoya,'):
            txtOutApi = txtText[:4]
            txtText = txtText[5:]
        if (txtText[:7] == 'google,'):
            txtOutApi = txtText[:6]
            txtText = txtText[7:]
        if (txtText[:5] == 'free,'):
            txtOutApi = txtText[:4]
            txtText = txtText[5:]

        if (txtText == ''):
            txtText = '!'

        if (True):
            if (txtText != '' and txtText != '!'):
                if (txtInpLang != txtOutLang):
                    qLogOutput(' ' + procId + ' Text Input   [' + txtText + '] ' + txtInpLang, True)

                recfile = txtInput.replace(qPathSTT, '')
                recfile = recfile.replace(qPathTRA, '')
                recfile = recfile.replace(qPathTTS, '')
                recfile = recfile.replace(qPathWork, '')
                recfile = qPathCtrl + recfile
                try:
                    w = codecs.open(recfile, 'w', 'utf-8')
                    w.write(txtText)
                    w.close()
                    w = None
                except:
                    w = None

    if (txtText != '' and txtInput != inpOutput):

        now = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d')
        recfile = qPathRec + fileId + '.tts.txt'
        recutf8 = qPathRec + '_' + stamp + '_tts_utf8.txt'
        recsjis = qPathRec + '_' + stamp + '_tts_sjis.txt'

        try:
            w = codecs.open(recfile, 'w', 'utf-8')
            w.write(txtText)
            w.close()
            w = None
        except:
            w = None

        try:
            a = codecs.open(recutf8, 'a', 'utf-8')
            a.write(fileId + ', [' + txtText + ']\n')
            a.close()
            a = None
        except:
            a = None

        try:
            a = codecs.open(recsjis, 'a', 'shift_jis')
            a.write(fileId + ', [' + txtText + ']\r\n')
            a.close()
            a = None
        except:
            a = None

    if (txtText != ''):
        txtWork = txtText

        if (txtInpLang != txtOutLang):
            txtWork,api = qTranslator(qApiTrn, txtInpLang, txtOutLang, txtText, )
            if (txtWork != '' and txtWork != '!'):
                if (api == qApiTrn) or (api == 'free' and qApiTrn == 'google'):
                        qLogOutput(' ' + procId + ' Text Trans   [' + txtWork + '] ' + txtOutLang + ' (' + api + ')', True)
                else:
                    if (api != ''):
                        qLogOutput(' ' + procId + ' Text Trans   [' + txtWork + '] ' + txtOutLang + ' (!' + api + ')', True)
                    else:
                        qLogOutput(' ' + procId + ' Text Trans   [' + txtWork + '] ' + txtOutLang + ' (!' + qApiTrn + ')', True)

                try:
                    w = codecs.open(qCtrlTranslate, 'w', 'utf-8')
                    w.write(txtOutLang + ', [' + txtWork + ']\n')
                    w.close()
                    w = None
                except:
                    w = None

        if (txtWork == ''):
            txtWork = '!'



    if (txtOutput != '' and txtWork != '!'):

        now = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d')
        recfile = qPathRec + fileId + '.tts.mp3'
        if (txtInput == inpOutput ):
            recfile = qPathRec + fileId + '.feedback.mp3'

        #qLogOutput(' ' + procId + ' Text Vocal   [' + txtWork + '] ' + txtOutLang + ' (' + qApiOut + ')', True)
        tmpfile = qPathWork + 'temp_qVoiceOutput.' + fileId + '.mp3'
        #res,api = qVoiceOutput(qApiOut, txtOutLang, txtWork, recfile, tmpfile)
        res,api = qVoiceOutput(txtOutApi, txtOutLang, txtWork, recfile, tmpfile)
        #if (api == qApiOut) or (api == 'free' and qApiOut == 'google'):
        if (api == txtOutApi) or (api == 'free' and txtOutApi == 'google'):
                qLogOutput(' ' + procId + ' Text Vocal   [' + txtWork + '] ' + txtOutLang + ' (' + api + ')', True)
        else:
            if (api != ''):
                qLogOutput(' ' + procId + ' Text Vocal   [' + txtWork + '] ' + txtOutLang + ' (!' + api + ')', True)
            else:
                qLogOutput(' ' + procId + ' Text Vocal   [' + txtWork + '] ' + txtOutLang + ' (!' + txtOutApi + ')', True)

        if (os.path.exists(recfile)):

            if (recfile[-4:].lower() == txtOutput[-4:].lower()):
                shutil.copy2(recfile, txtOutput)
            else:
                sox = subprocess.Popen(['sox', '-q', recfile, txtOutput, ], \
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

            if (txtPlay == 'on' or txtPlay == 'yes'):
                sox=subprocess.Popen(['sox', '-q', recfile, '-d', '--norm', ], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None



    if (outInput != ''):
        outRun  = True
        outText = ''

        if (outInput == inpOutput ):
            outText = inpText
        elif (outInput == trnOutput ):
            outText = trnText
        else:
            try:
                rt = codecs.open(outInput, 'r', 'utf-8')
                for t in rt:
                    outText = (outText + ' ' + str(t)).strip()
                rt.close
                rt = None
            except:
                rt = None

        if (outText == ''):
            outText = '!'



    if (outOutput != '' and outText != '!'):

        now = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d')
        if (inpInput != ''):
            recfile = qPathRec + fileId + '.vocalize.mp3'
            if (outInput == inpOutput ):
                recfile = qPathRec + fileId + '.feedback.mp3'
            elif (outInput == trnOutput ):
                recfile = qPathRec + fileId + '.translate.mp3'
        else:
            recfile = qPathRec + fileId + '.text2vocal.mp3'

        #qLogOutput(' ' + procId + ' Vocalization [' + outText + '] ' + qLangOut + ' (' + qApiOut + ')', True)
        tmpfile = qPathWork + 'temp_qVoiceOutput.' + fileId + '.mp3'
        res,api = qVoiceOutput(qApiOut, qLangOut, outText, recfile, tmpfile)
        if (api == qApiOut) or (api == 'free' and qApiOut == 'google'):
                if (inpInput != ''):
                    qLogOutput(' ' + procId + ' Vocalization [' + outText + '] ' + qLangOut + ' (' + api + ')', True)
                else:
                    qLogOutput(' ' + procId + ' Text Vocal   [' + outText + '] ' + qLangOut + ' (' + api + ')', True)
        else:
            if (api != ''):
                if (inpInput != ''):
                    qLogOutput(' ' + procId + ' Vocalization [' + outText + '] ' + qLangOut + ' (!' + api + ')', True)
                else:
                    qLogOutput(' ' + procId + ' Text Vocal   [' + outText + '] ' + qLangOut + ' (!' + api + ')', True)
            else:
                if (inpInput != ''):
                    qLogOutput(' ' + procId + ' Vocalization [' + outText + '] ' + qLangOut + ' (!' + qApiOut + ')', True)
                else:
                    qLogOutput(' ' + procId + ' Text Vocal   [' + outText + '] ' + qLangOut + ' (!' + qApiOut + ')', True)

        if (os.path.exists(recfile)):

            if (recfile[-4:].lower() == outOutput[-4:].lower()):
                shutil.copy2(recfile, outOutput)
            else:
                sox = subprocess.Popen(['sox', '-q', recfile, outOutput, ], \
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

            if (outPlay == 'on' or outPlay == 'yes'):
                sox=subprocess.Popen(['sox', '-q', recfile, '-d', '--norm', ], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None



    qLogOutput('___main___:terminate')

    qLogOutput('___main___:bye!')



