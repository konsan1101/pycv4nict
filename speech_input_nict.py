#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs



# nict 音声認識
import speech_api_nict     as nict_api
import speech_api_nict_key as nict_key



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
    print('speech_input_nict.py')
    print(' 1)inpLang = ' + str(inpLang))
    print(' 2)inpWave = ' + str(inpWave))
    print(' 3)inpText = ' + str(inpText))



    if os.path.exists(inpText):
        os.remove(inpText)



    resText = ''
    if (os.path.exists(inpWave)):

        #try:

        nictAPI = nict_api.SpeechAPI()
        res = nictAPI.authenticate('stt',
                   nict_key.getkey('stt', 'id' ),
                   nict_key.getkey('stt', 'key'), )
        if (res == True):

            resText, api = nictAPI.recognize(inpWave=inpWave, inpLang=inpLang)

        #except:
        #    pass



    print(' ' + resText)
    if (resText != ''):
        w = codecs.open(inpText, 'w', 'shift_jis')
        w.write(resText)
        w.close()
        w = None



