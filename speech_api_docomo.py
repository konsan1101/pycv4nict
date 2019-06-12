#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs
import subprocess

import requests
import json
import datetime



# docomo 音声認識,雑談対話,知識検索
import speech_api_docomo_key as docomo_key



class SpeechAPI:

    def __init__(self, ):
        self.timeOut         = 10
        self.stt_key         = None
        self.chatting_key    = None
        self.chatting_token  = None
        self.chatting_recv   = ''
        self.knowledge_key   = None
        self.knowledge_token = None
        self.knowledge_recv  = ''

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, key):
        # docomo 音声認識
        if (api == 'stt'):
            if (self.stt_key == None):
                self.stt_key = key
            if (not self.stt_key is None):
                return True

        # docomo 雑談対話
        if (api == 'chatting'):
            if (self.chatting_key   == None):
                self.chatting_key   = key
            if (self.chatting_token == None):
                url  = 'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/registration?APIKEY=' + self.chatting_key
                headers = {
                    'Content-Type': 'application/json;charset=UTF-8',
                    }
                data = {
                    'botId': 'Chatting',
                    'appKind': 'Smart Phone',
                    }
                try:
                    res = requests.post(url, headers=headers, data=json.dumps(data), timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        at = res.json()['appId']
                        self.chatting_token = at
                        #print(str(self.chatting_token))
                except:
                    self.chatting_token = None
            if (not self.chatting_token is None):
                return True

        # docomo 知識検索
        if (api == 'knowledge'):
            if (self.knowledge_key   == None):
                self.knowledge_key   = key
            if (self.knowledge_token == None):
                url  = 'https://api.apigw.smt.docomo.ne.jp/naturalKnowledge/v1/registration?APIKEY=' + self.knowledge_key
                headers = {
                    'Content-Type': 'application/json;charset=UTF-8',
                    }
                data = {
                    'botId': 'Knowledge',
                    'appKind': 'Smart Phone',
                    }
                try:
                    res = requests.post(url, headers=headers, data=json.dumps(data), timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        at = res.json()['appId']
                        self.knowledge_token = at
                        #print(str(self.knowledge_token))
                except:
                    self.knowledge_token = None
            if (not self.knowledge_token is None):
                return True

        return False

    def recognize(self, inpWave, inpLang='ja-JP', ):
        res_text = ''
        res_api  = ''
        if (self.stt_key == None):
            print('DOCOMO: Not Authenticate Error !')

        else:
            lang = ''
            if   (inpLang == 'ja') or (inpLang == 'ja-JP'):
                lang = 'ja-JP'

            if (lang != ''):
                try:

                    rb = open(inpWave, 'rb')
                    audio = rb.read()
                    rb.close
                    rb = None

                    url  = 'https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY=' + self.stt_key
                    file = {'a': audio, 'v':'on'}

                    res = requests.post(url, files=file, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        #print(res.text)
                        res_text = res.json()['text']
                        if (res_text != ''):
                            res_api = 'docomo'
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



    def chatting(self, inpText=u'お元気ですか', ):
        res_text = ''
        res_api  = ''
        if (self.chatting_token == None):
            print('DOCOMO: Not Authenticate Error !')

        else:
            inpLang = 'ja-JP'

            if (inpText != '') and (inpText != '!'):
                url  = 'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY=' + self.chatting_key
                headers = {
                    'Content-Type': 'application/json;charset=UTF-8',
                    }
                data = {
                    'language': inpLang,
                    'botId': 'Chatting',
                    'appId': self.chatting_token,
                    'voiceText': inpText,
                    'clientData': {
                      'option': {
                        'nickname': u'こんさん',
                        'nicknameY': u'こんさん',
                        'sex': u'男',
                        'bloodtype': 'A',
                        'birthdateY': 1965,
                        'birthdateM': 11,
                        'birthdateD': 1,
                        'age': 53,
                        'constellations': u'蠍座',
                        'mode': 'dialog',
                        ######'t': 'kansai',
                        }, },
                    'appRecvTime': self.chatting_recv,
                    'appSendTime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                    }
                try:
                    res = requests.post(url, headers=headers, data=json.dumps(data), timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        #print(res.text)
                        res_json = res.json()
                        res_recv = res_json['serverSendTime']
                        self.chatting_recv = res_recv
                        res_text = res_json['systemText']['expression']
                        res_api = 'docomo'
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

    def knowledge(self, inpText=u'姫路城の住所調べて', ):
        res_text = ''
        res_api  = ''
        if (self.knowledge_token == None):
            print('DOCOMO: Not Authenticate Error !')

        else:
            inpLang = 'ja-JP'

            if (inpText != '') and (inpText != '!'):
                url  = 'https://api.apigw.smt.docomo.ne.jp/naturalKnowledge/v1/dialogue?APIKEY=' + self.knowledge_key
                headers = {
                    'Content-Type': 'application/json;charset=UTF-8',
                    }
                data = {
                    'language': inpLang,
                    'botId': 'Knowledge',
                    'appId': self.knowledge_token,
                    'voiceText': inpText,
                    'appRecvTime': self.knowledge_recv,
                    'appSendTime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                    }
                try:
                    res = requests.post(url, headers=headers, data=json.dumps(data), timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        #print(res.text)
                        res_json = res.json()
                        res_recv = res_json['serverSendTime']
                        self.knowledge_recv = res_recv
                        res_text = res_json['systemText']['expression']
                        res_api = 'docomo'
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



if __name__ == '__main__':

        #docomoAPI = docomo_api.SpeechAPI()
        docomoAPI = SpeechAPI()

        res = docomoAPI.authenticate('stt', docomo_key.getkey('stt'), )
        print('authenticate:', res, )
        if (res == True):

            file='speech_api_docomo.wav'

            res, api = docomoAPI.recognize(inpWave=file, inpLang='ja-JP', )
            print('recognize:', res, '(' + api + ')' )



        print('testing code' )

        res2 = docomoAPI.authenticate('chatting', docomo_key.getkey('chatting'), )
        print('authenticate:', res2, )

        res3 = docomoAPI.authenticate('knowledge', docomo_key.getkey('knowledge'), )
        print('authenticate:', res3, )


        text = u'お元気ですか'
        print(text)
        res, api = docomoAPI.chatting(inpText=text, )
        print('chatting:', res, '(' + api + ')' )



        text = u'姫路城の住所調べて'
        print(text)
        res, api = docomoAPI.knowledge(inpText=text, )
        print('knowledge:', res, '(' + api + ')' )

        text = u'最寄り駅は'
        print(text)
        res, api = docomoAPI.knowledge(inpText=text, )
        print('knowledge:', res, '(' + api + ')' )

        text = u'今のロサンゼルスの時間調べて'
        print(text)
        res, api = docomoAPI.knowledge(inpText=text, )
        print('knowledge:', res, '(' + api + ')' )



