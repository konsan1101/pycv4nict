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
    print('narration1:init')
    print('narration1:start')
    print('narration1:proc')
    print('')



    inpFile = u'narration/1.入力テキスト_sjis.txt'
    if (os.path.exists(inpFile)):

        now=datetime.datetime.now()
        stamp=now.strftime('%Y%m%d.%H%M%S')
        seq = 0

        rt = codecs.open(inpFile, 'r', 'shift_jis')
        for t in rt:
            txt = str(t).strip()
            if (txt != '' and txt != '!'):

                print(txt)



                seq += 1
                nnnn = '{:04}'.format(seq)

                file = 'narration/tts/' + stamp + '.narration.' + nnnn + '.txt'

                try:
                    w = codecs.open(file, 'w', 'utf-8')
                    w.write(txt + '\r')
                    w.close
                    w = None
                except:
                    w = None



        rt.close
        rt = None



    print('')
    print('narration1:terminate')
    print('narration1:bye!')



