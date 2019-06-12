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
    print('gijiroku2:init')
    print('gijiroku2:start')
    print('gijiroku2:proc')
    print('')



    outFile = u'gijiroku/9.結果テキスト_sjis.txt'
    if (os.path.exists(outFile)):
        os.remove(outFile)



    files = glob.glob('gijiroku/stt/*.txt')

    for file in files:
        file = file.replace('\\', '/')
        fileId = file.replace('gijiroku/stt/', '')
        if (fileId[0:1] != '_'):
            print(fileId)

            txt = ''
            try:
                rt = codecs.open(file, 'r', 'utf-8')
                for t in rt:
                    txt = (txt + ' ' + str(t)).strip()
                rt.close
                rt = None
            except:
                rt = None

            try:
                a = codecs.open(outFile, 'a', 'shift_jis')
                a.write(fileId + ', [' + txt + ']\r\n')
                a.close()
                a = None
            except:
                a = None

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

                f1 = 'gijiroku/mp3/' + fileId[:-4] + '.mp3'
                f2 = 'gijiroku/mp3/' + fileId[:-4] + '.[' + f + '].mp3'
                try:
                    os.rename(f1, f2)
                except:
                    pass



    print('')
    print('gijiroku2:terminate')
    print('gijiroku2:bye!')



