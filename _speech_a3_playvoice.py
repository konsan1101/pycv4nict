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
import glob

print(os.path.dirname(__file__))
print(os.path.basename(__file__))
print(sys.version_info)



qPathCtrl  = 'temp/a3_0control/'
qPathInp   = 'temp/a3_1voice/'
qPathWav   = 'temp/a3_2stt_wav/'
qPathSTT   = 'temp/a3_3stt_txt/'
qPathTTS   = 'temp/a3_5tts_txt/'
qPathTRA   = 'temp/a3_6tra_txt/'
qPathPlay  = 'temp/a3_7play_voice/'
qPathRec   = 'temp/a3_8recorder/'
qPathWork  = 'temp/a3_9work/'

qBusyCtrl  = qPathWork + 'busy_speechctl.txt'
qBusyInput = qPathWork + 'busy_voice2wav.txt'
qBusySTT   = qPathWork + 'busy_sttcore.txt'
qBusyTTS   = qPathWork + 'busy_ttscore.txt'
qBusyPlay  = qPathWork + 'busy_playvoice.txt'



def qBusySet(file, sw=True):
    if (sw == True):
        chktime = time.time()
        while (not os.path.exists(file)) and ((time.time() - chktime) < 1):
            try:
                w = open(file, 'w')
                w.write('BUSY')
                w.close()
                w = None
            except:
                w = None
            time.sleep(0.10)
    else:
        chktime = time.time()
        while (os.path.exists(file)) and ((time.time() - chktime) < 1):
            try:
                os.remove(file)
            except:
                pass
            time.sleep(0.10)

def qBusyCheck(file, sec):
    chktime = time.time()
    while (os.path.exists(file)) and ((time.time() - chktime) < sec):
        time.sleep(0.10)
    if (os.path.exists(file)):
        return 'busy'
    else:
        return 'none'

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
def qLogOutput(pLogText='', pDisplay=True, pOutfile=True):
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

qMakeDirs('temp/_log/', False)
qLogOutput(qLogFlie, True, True)

def qGuide(tempFile=None, sync=True):
    if (tempFile == '_up'):
        tempFile = '_sound_up.mp3'
    if (tempFile == '_ready'):
        tempFile = '_sound_ready.mp3'
    if (tempFile == '_accept'):
        tempFile = '_sound_accept.mp3'
    if (tempFile == '_ok'):
        tempFile = '_sound_ok.mp3'
    if (tempFile == '_ng'):
        tempFile = '_sound_ng.mp3'
    if (tempFile == '_down'):
        tempFile = '_sound_down.mp3'
    if (tempFile == '_shutter'):
        tempFile = '_sound_shutter.mp3'

    if (os.path.exists(tempFile)):

        sox=subprocess.Popen(['sox', '-q', tempFile, '-d', ], \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        if (sync == True):
            sox.wait()
            sox.terminate()
            sox = None



playvoice_start=0
playvoice_beat =0
playvoice_busy =False
playvoice_last =0
playvoice_seq  =0
def proc_playvoice(cn_r, cn_s, ):
    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    global qBusyCtrl
    global qBusyInput
    global qBusySTT
    global qBusyTTS
    global qBusyPlay

    global playvoice_start
    global playvoice_beat
    global playvoice_busy
    global playvoice_last

    global playvoice_seq

    qLogOutput('play_voice:init')

    runMode  = cn_r.get()
    micDev   = cn_r.get()
    micType  = cn_r.get()
    micGuide = cn_r.get()
    cn_r.task_done()

    qLogOutput('play_voice:runMode =' + str(runMode ))
    qLogOutput('play_voice:micDev  =' + str(micDev  ))
    qLogOutput('play_voice:micType =' + str(micType ))
    qLogOutput('play_voice:micGuide=' + str(micGuide))

    qLogOutput('play_voice:start')
    playvoice_start=time.time()

    while (True):
        playvoice_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('playvoice_:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qLogOutput('playvoice_: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                #playvoice_last = time.time()
                cn_s.put(['PASS', ''])

            else:

                playvoice_busy = True

                result = 'OK'

                files = glob.glob(qPathPlay + '*')
                if (len(files) > 0):

                    qBusySet(qBusyPlay, True)

                    #qBusyCheck(qBusyCtrl, 3)
                    #qBusyCheck(qBusySTT , 3)
                    #qBusyCheck(qBusyTTS , 3)
                    #qBusyCheck(qBusyPlay, 3)
                    if (micType == 'bluetooth') or (micGuide == 'on' or micGuide == 'sound'):
                        qBusyCheck(qBusyInput, 3)

                path=qPathPlay
                files = glob.glob(path + '*')
                if (len(files) > 0):

                    try:
                        for f in files:
                            file=f.replace('\\', '/')
                            if (file[-4:].lower() == '.wav' and file[-8:].lower() != '.tmp.wav'):
                                f1=file
                                f2=file[:-4] + '.tmp.wav'
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass
                            if (file[-4:].lower() == '.mp3' and file[-8:].lower() != '.tmp.mp3'):
                                f1=file
                                f2=file[:-4] + '.tmp.mp3'
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                            if (file[-8:].lower() == '.tmp.wav' or file[-8:].lower() == '.tmp.mp3'):
                                f1=file
                                f2=file[:-8] + file[-4:]
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                                fileId = file.replace(path, '')
                                fileId = fileId[:-4]

                                playvoice_seq += 1
                                if (playvoice_seq >= 10000):
                                    playvoice_seq = 1
                                seq4 = '{:04}'.format(playvoice_seq)
                                seq2 = seq4[-2:]

                                wrkfile = qPathWork + 'playvoice.' + seq2 + '.mp3'
                                if (os.path.exists(wrkfile)):
                                    try:
                                        os.remove(wrkfile)
                                    except:
                                        pass

                                sox=subprocess.Popen(['sox', '-q', file, wrkfile, ], \
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                                sox.wait()
                                sox.terminate()
                                sox = None

                                if (str(micDev) != 'file'):
                                    os.remove(file)

                                if (os.path.exists(wrkfile)):

                                    if (runMode == 'debug' or str(micDev) == 'file'):
                                        qLogOutput('play_voice:' + fileId + u' → ' + wrkfile[:-4])

                                    playvoice_last = time.time()

                                    sox=subprocess.Popen(['sox', '-q', wrkfile, '-d', '--norm', ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                                    #if (str(micDev) == 'file'):
                                    if (runMode=='debug' or runMode=='handsfree'):
                                        sox.wait()
                                        sox.terminate()
                                        sox = None

                    except:
                        pass
                        result = 'NG'

                if (str(micDev) == 'file'):
                    if (result == 'OK'):
                        cn_s.put(['END', ''])
                        time.sleep( 5.00)
                        break
                    else:
                        cn_s.put(['ERROR', ''])
                        time.sleep( 5.00)
                        break
                else:
                    cn_s.put([result, ''])

        playvoice_busy = False
        qBusySet(qBusyPlay, False)

        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.05)

    qLogOutput('play_voice:terminate')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('play_voice:end')



def main_init(micDev, ):
    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    global qBusyCtrl
    global qBusyInput
    global qBusySTT
    global qBusyTTS
    global qBusyPlay

    qMakeDirs('temp/_log/',   False)
    qMakeDirs('temp/_cache/', False)

    if (str(micDev) != 'file'):
        qMakeDirs(qPathCtrl, False)
        qMakeDirs(qPathInp,  False)
        qMakeDirs(qPathWav,  False)
        qMakeDirs(qPathSTT,  False)
        qMakeDirs(qPathTTS,  False)
        qMakeDirs(qPathTRA,  False)
        qMakeDirs(qPathPlay, True )
        qMakeDirs(qPathRec,  False)
        qMakeDirs(qPathWork, False)
    else:
        qMakeDirs(qPathCtrl, False)
        qMakeDirs(qPathInp,  False)
        qMakeDirs(qPathWav,  False)
        qMakeDirs(qPathSTT,  False)
        qMakeDirs(qPathTTS,  False)
        qMakeDirs(qPathTRA,  False)
        qMakeDirs(qPathPlay, False)
        qMakeDirs(qPathRec,  False)
        qMakeDirs(qPathWork, False)

    qBusySet(qBusyCtrl,  False )
    qBusySet(qBusyInput, False )
    qBusySet(qBusySTT,   False )
    qBusySet(qBusyTTS,   False )
    qBusySet(qBusyPlay,  False )



main_start=0
main_beat =0
main_busy =False
main_last =0
if (__name__ == '__main__'):
    #global main_beat
    #global playvoice_beat

    qLogOutput('')
    qLogOutput('play_main_:init')
    qLogOutput('play_main_:exsample.py runMode, mic..., ')
    #runMode  handsfree, translator, speech, ...,
    #micDev   num or file
    #micType  usb or bluetooth
    #micGuide off, on, display, sound

    runMode  = 'debug'
    micDev   = '0'
    micType  = 'usb'
    micGuide = 'on'
    micLevel = '777'

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        micDev   = str(sys.argv[2]).lower()
    if (len(sys.argv) >= 4):
        micType  = str(sys.argv[3]).lower()
    if (len(sys.argv) >= 5):
        micGuide = str(sys.argv[4]).lower()
    if (len(sys.argv) >= 6):
        p = str(sys.argv[5]).lower()
        if (p.isdigit() and p != '0'):
            micLevel = p

    qLogOutput('')
    qLogOutput('play_main_:runMode  =' + str(runMode  ))
    qLogOutput('play_main_:micDev   =' + str(micDev   ))
    qLogOutput('play_main_:micType  =' + str(micType  ))
    qLogOutput('play_main_:micGuide =' + str(micGuide ))
    qLogOutput('play_main_:micLevel =' + str(micLevel ))

    main_init(micDev, )

    qLogOutput('')
    qLogOutput('play_main_:start')
    main_start     = time.time()
    main_beat      = 0

    playvoice_s    = queue.Queue()
    playvoice_r    = queue.Queue()
    playvoice_proc = None
    playvoice_beat = 0
    playvoice_pass = 0

    while (True):
        main_beat = time.time()

        # check voice2wav_last

        if (str(micDev) == 'file'):
            if (playvoice_last == 0):
                playvoice_last = time.time()
            sec = int(time.time() - playvoice_last)
            if (sec > 90):
                break

        # Thread timeout check

        if (playvoice_beat != 0):
          if (str(micDev) != 'file'):
            sec = int(time.time() - playvoice_beat)
            if (sec > 60):
                qLogOutput('play_main_:playvoice_proc 60s')
                qLogOutput('play_main_:playvoice_proc break')
                playvoice_s.put([None, None])
                time.sleep(3.00)
                playvoice_proc = None
                playvoice_beat = 0
                playvoice_pass = 0

                #kill = subprocess.Popen(['_speech_a3_kill_sox.bat', ], \
                #       stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                #kill.wait()
                #kill.terminate()
                #kill = None

        # Thread start

        if (playvoice_proc is None):
            while (playvoice_s.qsize() > 0):
                dummy = playvoice_s.get()
            while (playvoice_r.qsize() > 0):
                dummy = playvoice_r.get()
            playvoice_proc = threading.Thread(target=proc_playvoice, args=(playvoice_s,playvoice_r,))
            playvoice_proc.daemon = True
            playvoice_s.put(runMode )
            playvoice_s.put(micDev  )
            playvoice_s.put(micType )
            playvoice_s.put(micGuide)
            playvoice_proc.start()
            time.sleep(1.00)

            playvoice_s.put(['START', ''])

        # processing

        if (playvoice_r.qsize() == 0 and playvoice_s.qsize() == 0):
            playvoice_s.put(['PROC', ''])
            playvoice_pass += 1
        else:
            playvoice_pass = 0
        if (playvoice_pass > 50):
            playvoice_s.put(['PASS', ''])
            playvoice_pass = 0

        break_flag = False
        while (playvoice_r.qsize() > 0):
            playvoice_get = playvoice_r.get()
            playvoice_res = playvoice_get[0]
            playvoice_dat = playvoice_get[1]
            playvoice_r.task_done()
            if (playvoice_res == 'END'):
                break_flag = True
            if (playvoice_res == 'ERROR'):
                break_flag = True
        #if (break_flag == True):
        #    break



        time.sleep(0.05)



    qLogOutput('')
    qLogOutput('play_main_:terminate')

    try:
        playvoice_s.put( [None, None] )
        time.sleep(3.00)
    except:
        pass

    try:
        playvoice_proc.join()
    except:
        pass

    qBusySet(qBusyPlay, False)

    qLogOutput('play_main_:bye!')


