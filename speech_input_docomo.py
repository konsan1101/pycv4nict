#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs



# docomo 音声認識
import speech_api_docomo     as docomo_api
import speech_api_docomo_key as docomo_key



if __name__ == '__main__':

    inpLang = 'ja'
    inpWave = 'temp/temp_inpWave.wav'
    inpText = 'temp/temp_inpText.txt'

    if (len(sys.argv) >= 2):
        inpLang = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpWave = sys.argv[2]
    if (len(sys.argv) >= 4):
        inpText = sys.argv[3]



    print('')
    print('speech_input_docomo.py')
    print(' 1)inpLang = ' + str(inpLang))
    print(' 2)inpWave = ' + str(inpWave))
    print(' 3)inpText = ' + str(inpText))



    if os.path.exists(inpText):
        os.remove(inpText)



    resText = ''
    if (os.path.exists(inpWave)):

        #try:

        docomoAPI = docomo_api.SpeechAPI()
        res = docomoAPI.authenticate('stt', docomo_key.getkey('stt'), )
        if (res == True):

            resText, api = docomoAPI.recognize(inpWave=inpWave, inpLang=inpLang)

        #except:
        #    pass



    print(' ' + resText)
    if (resText != ''):
        w = codecs.open(inpText, 'w', 'shift_jis')
        w.write(resText)
        w.close()
        w = None



