#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs
import subprocess

import requests
import json



# nict 音声認識、翻訳機能、音声合成
import speech_api_nict_key as nict_key



class SpeechAPI:

    def __init__(self, ):
        self.timeOut   = 10
        self.stt_token = None
        self.tra_token = None
        self.tts_token = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, id, key, ):
        #説明 https://mimi.readme.io/page/tagengo
        #curl -X POST https://auth.mimi.fd.ai/v2/token
        #--form-string grant_type="https://auth.mimi.fd.ai/grant_type/application_credentials"
        #--form-string client_id="…"
        #--form-string client_secret="…"
        #--form-string scope="https://apis.mimi.fd.ai/auth/nict-tts/http-api-service;https://apis.mimi.fd.ai/auth/nict-tra/http-api-service;https://apis.mimi.fd.ai/auth/nict-asr/http-api-service;https://apis.mimi.fd.ai/auth/nict-asr/websocket-api-service;https://apis.mimi.fd.ai/auth/applications.r"

        # nict 音声認識
        if (api == 'stt'):
            if (self.stt_token == None):
                url  = 'https://auth.mimi.fd.ai/v2/token'
                params = {
                    'grant_type': 'https://auth.mimi.fd.ai/grant_type/application_credentials',
                    'client_id': str(id),
                    'client_secret': str(key),
                    'scope': 'https://apis.mimi.fd.ai/auth/nict-tts/http-api-service;https://apis.mimi.fd.ai/auth/nict-tra/http-api-service;https://apis.mimi.fd.ai/auth/nict-asr/http-api-service;https://apis.mimi.fd.ai/auth/nict-asr/websocket-api-service;https://apis.mimi.fd.ai/auth/applications.r',
                    }
                try:
                    res = requests.post(url, params=params, timeout=self.timeOut, )
                    #print(res)
                    at = res.json()['accessToken']
                    self.stt_token = at
                    #print('NICT:' + str(self.stt_token))
                except:
                    self.stt_token = None
            if (not self.stt_token is None):
                return True

        # nict 翻訳機能
        if (api == 'tra'):
            if (self.tra_token == None):
                url  = 'https://auth.mimi.fd.ai/v2/token'
                params = {
                    'grant_type': 'https://auth.mimi.fd.ai/grant_type/application_credentials',
                    'client_id': str(id),
                    'client_secret': str(key),
                    'scope': 'https://apis.mimi.fd.ai/auth/nict-tts/http-api-service;https://apis.mimi.fd.ai/auth/nict-tra/http-api-service;https://apis.mimi.fd.ai/auth/nict-asr/http-api-service;https://apis.mimi.fd.ai/auth/nict-asr/websocket-api-service;https://apis.mimi.fd.ai/auth/applications.r',
                    }
                try:
                    res = requests.post(url, params=params, timeout=self.timeOut, )
                    #print(res)
                    at = res.json()['accessToken']
                    self.tra_token = at
                    #print('NICT:' + str(self.tra_token))
                except:
                    self.tra_token = None
            if (not self.tra_token is None):
                return True

        # nict 音声合成
        if (api == 'tts'):
            if (self.tts_token == None):
                url  = 'https://auth.mimi.fd.ai/v2/token'
                params = {
                    'grant_type': 'https://auth.mimi.fd.ai/grant_type/application_credentials',
                    'client_id': str(id),
                    'client_secret': str(key),
                    'scope': 'https://apis.mimi.fd.ai/auth/nict-tts/http-api-service;https://apis.mimi.fd.ai/auth/nict-tra/http-api-service;https://apis.mimi.fd.ai/auth/nict-asr/http-api-service;https://apis.mimi.fd.ai/auth/nict-asr/websocket-api-service;https://apis.mimi.fd.ai/auth/applications.r',
                    }
                try:
                    res = requests.post(url, params=params, timeout=self.timeOut, )
                    #print(res)
                    at = res.json()['accessToken']
                    self.tts_token = at
                    #print('NICT:' + str(self.tts_token))
                except:
                    self.tts_token = None
            if (not self.tts_token is None):
                return True

        return False

    def ticketRemained(self, ):
        #説明 https://mimi.readme.io/page/tagengo
        #curl https://apis.mimi.fd.ai/v1/applications/counter
        #-H "Authorization: Bearer <token-key>"

        if (self.stt_token == None):
            print('NICT: Not Authenticate Error !')

        else:

                    url  = 'https://apis.mimi.fd.ai/v1/applications/counter'
                    headers = {
                        'Authorization': 'Bearer ' + self.stt_token,
                        }
                    res = requests.get(url, headers=headers, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        #print(res.text)
                        res_json = json.loads(res.text)
                        res_text = res_json[0]['counts']['ticket_remained']
                        res_text = str(res_text).strip()
                        return res_text, 'nict'

        return '', ''

    def recognize(self, inpWave, inpLang='ja', api='auto', ):
        res_text = ''
        res_api  = ''

        #説明 https://mimi.readme.io/docs/asr-quickstart
        #curl https://service.mimi.fd.ai
        #-H "Content-Type: audio/x-pcm;bit=16;rate=16000;channels=1"
        #-H "x-mimi-process:nict-asr" nict-asr,google-asr,asr
        #-H "x-mimi-input-language:ja"
        #-H "Authorization: Bearer <token-key>"
        #--data-binary @$HOME/dev/libmimiio/examples/audio.raw

        if (self.stt_token == None):
            print('NICT: Not Authenticate Error !')

        else:
            if (True):
                try:
                    rb = open(inpWave, 'rb')
                    audio = rb.read()
                    rb.close
                    rb = None

                    if (res_text == '') and (api == 'auto' or api == 'asr' or api == 'nict-asr'):
                        url  = 'https://service.mimi.fd.ai'
                        if (api == 'asr'):
                            headers = {
                                'Content-Type': 'audio/x-pcm;bit=16;rate=16000;channels=1',
                                'x-mimi-process': 'asr',
                                'x-mimi-input-language': inpLang,
                                'Authorization': 'Bearer ' + self.stt_token,
                                }
                            res_api = 'nict(asr)'
                        else:
                            headers = {
                                'Content-Type': 'audio/x-pcm;bit=16;rate=16000;channels=1',
                                'x-mimi-process': 'nict-asr',
                                'x-mimi-input-language': inpLang,
                                'Authorization': 'Bearer ' + self.stt_token,
                                }
                            res_api = 'nict'
                        res = requests.post(url, headers=headers, data=audio, timeout=self.timeOut, )
                        #print(res)
                        if (res.status_code == 200):
                            res_json = json.loads(res.text)
                            res_text = ''
                            for sentence in res_json['response']:
                                res_t = sentence['result']
                                res_split = res_t.split('|')
                                if (inpLang=='ja') or (inpLang=='ja-JP'):
                                    res_text += res_split[0]
                                else:
                                    res_text += ' ' + res_split[0]
                        if (res_text == ''):
                            res_api = ''

                    if (res_text == '') and (api == 'auto' or api == 'google-asr'):
                        url  = 'https://service.mimi.fd.ai'
                        headers = {
                            'Content-Type': 'audio/x-pcm;bit=16;rate=16000;channels=1',
                            'x-mimi-process': 'google-asr',
                            'x-mimi-input-language': inpLang,
                            'Authorization': 'Bearer ' + self.stt_token,
                            }
                        res = requests.post(url, headers=headers, data=audio, timeout=self.timeOut, )
                        #print(res)
                        if (res.status_code == 200):
                            res_json = json.loads(res.text)
                            res_text = ''
                            for sentence in res_json['response']:
                                res_t = sentence['result']
                                res_split = res_t.split('|')
                                if (inpLang=='ja') or (inpLang=='ja-JP'):
                                    res_text += res_split[0]
                                else:
                                    res_text += ' ' + res_split[0]
                            if (res_text != ''):
                                res_api = 'nict(google)'
                except:
                    pass

            if (res_text != ''):
                res_text = str(res_text).strip()
                while (res_text[-1:] == u'。') \
                   or (res_text[-1:] == u'、') \
                   or (res_text[-1:] == '.'):
                    res_text = res_text[:-1]

                if (inpLang == 'ja' or inpLang == 'ja-JP'):
                    chk_text = str(res_text).replace(' ', '')
                    chk_text = str(chk_text).replace('.', '')
                    chk_text = str(chk_text).replace('_', '')
                    if (not chk_text.encode('utf-8').isalnum()):
                        res_text = str(res_text).replace(' ', '')

                return res_text, res_api

        return '', ''

    def translate(self, inpText=u'こんにちは', inpLang='ja', outLang='en', ):
        res_text = ''
        res_api  = ''

        #説明 https://mimi.readme.io/docs/tra-quickstart
        #curl https://tra.mimi.fd.ai/machine_translation
        #-H "Authorization: Bearer <token-key>"
        #-d text=こんにちは
        #-d source_lang=ja
        #-d target_lang=en

        if (self.tra_token == None):
            print('NICT: Not Authenticate Error !')

        else:
            if (inpText != '') and (inpText != '!'):
                try:

                    url  = 'https://tra.mimi.fd.ai/machine_translation'
                    headers = {
                        'Authorization': 'Bearer ' + self.tra_token,
                        }
                    params = {
                        'text': inpText,
                        'source_lang': inpLang,
                        'target_lang': outLang,
                        }
                    res = requests.get(url, headers=headers, params=params, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        res_json = json.loads(res.text)
                        res_text = res_json[0]
                        if (res_text != ''):
                            res_api = 'nict'
                except:
                    pass

            if (res_text != ''):
                res_text = str(res_text).strip()
                while (res_text[-1:] == u'。') \
                   or (res_text[-1:] == u'、') \
                   or (res_text[-1:] == '.'):
                    res_text = res_text[:-1]

                if (outLang == 'ja' or outLang == 'ja-JP'):
                    chk_text = str(res_text).replace(' ', '')
                    chk_text = str(chk_text).replace('.', '')
                    chk_text = str(chk_text).replace('_', '')
                    if (not chk_text.encode('utf-8').isalnum()):
                        res_text = str(res_text).replace(' ', '')

                return res_text, res_api

        return '', ''

    def vocalize(self, outText='hallo', outLang='en', outGender='female', outFile='temp_voice.wav', ):
        #説明 https://mimi.readme.io/docs/srs-quickstart
        #curl https://tts.mimi.fd.ai/speech_synthesis
        #-H "Authorization: Bearer <token-key>"
        #-d text=こんにちは
        #-d engine=nict
        #-d lang=ja > test.wav; play test.wav

        if (self.tts_token == None):
            print('NICT: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except:
                    pass

            if (outText != '') and (outText != '!'):
                try:

                    url  = 'https://tts.mimi.fd.ai/speech_synthesis'
                    headers = {
                        'Authorization': 'Bearer ' + self.tts_token,
                        }
                    params = {
                        'text': outText,
                        'engine': 'nict',
                        'lang': outLang,
                        'gender': outGender.lower(),
                        'age': '18',
                        }
                    res = requests.get(url, headers=headers, params=params, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        wb = open(outFile, 'wb')
                        wb.write(res.content)
                        wb.close()
                        wb = None
                        return outText, 'nict'

                except:
                    pass
        return '', ''



if __name__ == '__main__':

        #nictAPI = nict_api.SpeechAPI()
        nictAPI = SpeechAPI()

        res1 = nictAPI.authenticate('stt',
                    nict_key.getkey('stt','id'),
                    nict_key.getkey('stt','key'), )
        res2 = nictAPI.authenticate('tra',
                    nict_key.getkey('tra','id'),
                    nict_key.getkey('tra','key'), )
        res3 = nictAPI.authenticate('tts',
                    nict_key.getkey('tts','id'),
                    nict_key.getkey('tts','key'), )
        print('authenticate:', res1, res2, res3)
        if (res1 == True) and (res2 == True) and (res3 == True):

            res, api = nictAPI.ticketRemained()
            print('ticketRemained:', res)

            text = res
            file = 'temp_voice.wav'

            res, api = nictAPI.vocalize(outText=text, outLang='en', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'])
            sox.wait()
            sox.terminate()
            sox = None

            res, api = nictAPI.recognize(inpWave=file, inpLang='en', api='auto', )
            print('recognize:', res, '(' + api + ')' )

            res, api = nictAPI.translate(inpText=res, inpLang='en', outLang='ja', )
            print('translate:', res, '(' + api + ')' )



