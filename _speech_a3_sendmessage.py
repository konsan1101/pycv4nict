# -*- coding: utf-8 -*-
import sys
import os
import datetime
import time
import codecs

import ctypes
import array



WM_CHAR = 0x0102

def enum_child_windows_proc(handle, list):
    list.append(handle)
    return 1



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

if __name__ == "__main__":
    qLogOutput('___main___:init')
    qLogOutput('___main___:exsample.py txtFile, winTitle ')

    txtFile   = '_speech_a3_sendmessage.py'
    winTitle  = u'無題 - メモ帳'

    if (len(sys.argv) >= 2):
        txtFile   = sys.argv[1]
    if (len(sys.argv) >= 3):
        winTitle  = sys.argv[2]

    qLogOutput('')
    qLogOutput('___main___:txtFile  =' + str(txtFile  ))
    qLogOutput('___main___:winTitle =' + str(winTitle ))

    parent_handle = ctypes.windll.user32.FindWindowW(0, winTitle)

    if (parent_handle == 0):
        #qLogOutput('winTitle "' + winTitle + '" is not found !', True)
        qLogOutput('winTitle "' + winTitle + '" is not found !')

    else:

        child_handles = array.array('i')
        ENUM_CHILD_WINDOWS = ctypes.WINFUNCTYPE( \
                             ctypes.c_int, \
                             ctypes.c_int, \
                             ctypes.py_object)
        ctypes.windll.user32.EnumChildWindows( \
                             parent_handle, \
                             ENUM_CHILD_WINDOWS(enum_child_windows_proc), \
                             ctypes.py_object(child_handles) )

        try:
            rt = codecs.open(txtFile, 'r', 'utf-8')
            for txt in rt:
                txt = txt.replace('\r', '')
                txt = txt.replace('\n', '')
                txt += '\n'
                for i in range(len(txt)):
                    ctypes.windll.user32.SendMessageW(child_handles[0], WM_CHAR, (ord(txt[i])), 0)
            rt.close
            rt = None
        except:
            rt = None



    qLogOutput('___main___:terminate')
    qLogOutput('___main___:bye!')



