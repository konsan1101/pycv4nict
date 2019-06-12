#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import datetime
import time
import codecs
import glob
import shutil



if __name__ == '__main__':
    print('narration2:init')
    print('narration2:start')
    print('narration2:proc')
    print('')



    files = glob.glob('narration/mp3/*.mp3')

    for file in files:
        file = file.replace('\\', '/')
        fileId = file.replace('narration/mp3/', '')
        fileId = fileId.replace('.text2vocal', '')

        if (True):
            print(fileId)

            f1 = file
            f2 = 'narration/wav/' + fileId[:-4] + '.text2vocal.wav'
            try:
                sox = subprocess.Popen(['sox', '-q', f1, '-r', '16000', '-b', '16', '-c', '1', f2, ], \
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None
            except:
                pass

            txt = ''
            file2 = 'narration/tts/' + fileId[:-4] + '.txt'

            if (os.path.exists(file2)):
                try:
                    rt = codecs.open(file2, 'r', 'utf-8')
                    for t in rt:
                        txt = (txt + ' ' + str(t)).strip()
                    rt.close
                    rt = None
                except:
                    rt = None

            if (txt != ''):

                f = txt.replace(' ','_')
                f = f.replace(u'　','_')
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
                if (len(f)>100):
                    f = f[:100] + u'…'

                f1 = 'narration/mp3/' + fileId[:-4] + '.text2vocal.mp3'
                f2 = 'narration/mp3/' + fileId[:-4] + '.[' + f + '].mp3'
                try:
                    os.rename(f1, f2)
                except:
                    pass

                f1 = 'narration/wav/' + fileId[:-4] + '.text2vocal.wav'
                f2 = 'narration/wav/' + fileId[:-4] + '.[' + f + '].wav'
                try:
                    os.rename(f1, f2)
                except:
                    pass



    print('')
    print('narration2:terminate')
    print('narration2:bye!')



