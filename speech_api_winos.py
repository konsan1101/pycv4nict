#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs
import subprocess

import platform
qOS = platform.system().lower() #windows,darwin,linux

if (qOS == 'windows'):
    import win32com.client as wincl
    import win32api



# winos 音声合成



class SpeechAPI:

    def __init__(self, ):
        self.system = None

    def authenticate(self, ):
        self.system = platform.system().lower() #windows,darwin,linux
        if (self.system == 'windows'):
            return True
        return False

    def vocalize(self, outText='hallo', outLang='en-US', outGender='female', outFile='temp_voice.wav'):
        if (self.system == None):
            print('WINOS: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except:
                    pass

            #ja-JP:日本語〇,    en-US:英語〇,
            #ar-AR:アラビア語x, es-ES:スペイン語×, de-DE:ドイツ語×
            #fr-FR:フランス語〇,it-IT:イタリア語×, pt-BR:ポルトガル語×
            #ru-RU:ロシア語×,  tr-TR:トルコ語×,   uk-UK:ウクライナ語×
            #zh-CN:中国語×,    kr-KR:韓国語×

            lang = ''
            if   (outLang == 'ja') or (outLang == 'ja-JP'):
                lang = 'ja-JP'
            elif (outLang == 'en') or (outLang == 'en-US'):
                lang = 'en-US'
            elif (outLang == 'ar'):
                lang = 'ar-AR'
            elif (outLang == 'es'):
                lang = 'es-ES'
            elif (outLang == 'de'):
                lang = 'de-DE'
            elif (outLang == 'fr'):
                lang = 'fr-FR'
            elif (outLang == 'it'):
                lang = 'it-IT'
            elif (outLang == 'pt'):
                lang = 'pt-BR'
            elif (outLang == 'ru'):
                lang = 'ru-RU'
            elif (outLang == 'tr'):
                lang = 'tr-TR'
            elif (outLang == 'uk'):
                lang = 'uk-UK'
            elif (outLang == 'zh') or (outLang == 'zh-CN'):
                lang = 'zh-CN'
            elif (outLang == 'kr'):
                lang = 'kr-KR'

            if (lang != '') and (outText != '') and (outText != '!'):

                try:
                    # MS Windows
                    stml  = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
                    stml += '<voice xml:lang="' + lang + '" gender="' + outGender.lower() + '">'
                    stml += outText
                    stml += '</voice></speak>'

                    engine = wincl.Dispatch('SAPI.SpVoice')
                    #engine.Speak(stml)

                    stream = wincl.Dispatch('SAPI.SpFileStream')
                    stream.open(outFile, 3, False)
                    #for speaker in engine.GetAudioOutputs():
                    #    print(speaker.GetDescription())
                    engine.AudioOutputStream = stream
                    engine.Speak(stml)
                    stream.close()

                    if (os.path.exists(outFile)):
                        rb = open(outFile, 'rb')
                        size = sys.getsizeof(rb.read())
                        if (size <= 44):
                            os.remove(outFile)
                        else:
                            return outText, 'winos'
                except:
                    pass

        return '', ''



if __name__ == '__main__':

        #winosAPI = winos_api.SpeechAPI()
        winosAPI = SpeechAPI()

        res = winosAPI.authenticate()
        if (res == True):

            text = 'Hallo!'
            file = 'temp_voice.wav'

            res, api = winosAPI.vocalize(outText=text, outLang='en-US', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'])
            sox.wait()
            sox.terminate()
            sox = None



