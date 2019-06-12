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

import platform
qOS = platform.system().lower() #windows,darwin,linux

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

def qKill(pName, ):
    if (os.name == 'nt'):
        try:
            kill = subprocess.Popen(['taskkill', '/im', pName + '.exe', '/f', ], \
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            kill.wait()
            kill.terminate()
            kill = None
        except:
            pass
    else:
        try:
            kill = subprocess.Popen(['pkill', '-9', '-f', pName, ], \
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            kill.wait()
            kill.terminate()
            kill = None
        except:
            pass

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



julius_start= 0
julius_beat = 0
julius_busy = False
julius_last = 0
julius_bakSEQ  = 0
julius_bakLast = ''
julius_bakWav  = ''

adinsvr_run = False
adinsvr_sbp = None
adinexe_run = False
adinexe_sbp = None
adingui_run = False
adingui_sbp = None
bakSox_run  = False
bakSox_sbp  = None

def proc_julius(cn_r, cn_s, ):
    global qOS

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

    global julius_start
    global julius_beat
    global julius_busy
    global julius_last
    global julius_bakSEQ
    global julius_bakLast
    global julius_bakWav

    global adinsvr_run
    global adinsvr_sbp
    global adinexe_run
    global adinexe_sbp
    global adingui_run
    global adingui_sbp
    global bakSox_run
    global bakSox_sbp

    global v2w_wave_seq

    qLogOutput('julius____:init')

    runMode  = cn_r.get()
    micDev   = cn_r.get()
    micType  = cn_r.get()
    micGuide = cn_r.get()
    micLevel = cn_r.get()
    cn_r.task_done()

    #qLogOutput('julius____:runMode =' + str(runMode ))
    #qLogOutput('julius____:micDev  =' + str(micDev  ))
    #qLogOutput('julius____:micType =' + str(micType ))
    #qLogOutput('julius____:micGuide=' + str(micGuide))
    #qLogOutput('julius____:micLevel=' + str(micLevel))

    qLogOutput('julius____:start')
    julius_start=time.time()

    julius_rewind   = '555'
    julius_headmg   = '333'
    julius_tailmg   = '444'
    vadLevel        = '1'
    if (micLevel == '1'):
        vadLevel    = '3'



    if (str(micDev) != 'file'):
        if (bakSox_run == True):
            bakSox_run = False
            if (not bakSox_sbp is None):
                try:
                    stdout, stderr = bakSox_sbp.communicate()
                except:
                    pass
                bakSox_sbp.wait(2)
                bakSox_sbp.terminate()
                bakSox_sbp = None

        if (julius_bakLast != '' and julius_bakWav != ''):
            if (os.path.exists(julius_bakWav)):
                qLogOutput('julius____:recovery ' + julius_bakLast)

                #shutil.copy2(julius_bakWav, julius_bakLast)
                sox = subprocess.Popen(['sox', '-q', julius_bakWav, julius_bakLast, ], \
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

                try:
                    time.sleep(0.20)
                    os.remove(julius_bakWav)
                except:
                    pass

        julius_bakLast = ''
        julius_bakWav  = ''

        julius_bakSEQ  = 9999 #dummy



    while (True):
        julius_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('julius____:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qLogOutput('julius____: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                julius_last = time.time()
                cn_s.put(['PASS', ''])

            else:

                julius_busy = True
                julius_last = time.time()

                if (str(micDev) != 'file') and (adinsvr_run == False):
                    adinsvr_run = True
                    #now=datetime.datetime.now()
                    #filename=qPathInp + now.strftime('%H%M%S') +'.julius'
                    #adinsvr_sbp = subprocess.Popen(['adintool', '-in', 'adinnet', '-out', 'file', '-filename', filename, '-startid', '5001',] , \
                    #              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    #              #stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
                    #time.sleep(0.50)
                    if (micGuide != 'off'):
                        qGuide('_up')

                sw = 'off'
                if (str(micDev) != 'file'):
                    if (micType == 'usb'):
                        sw = 'on'
                    else:
                        if  (qBusyCheck(qBusyCtrl, 1) != 'busy') \
                        and (qBusyCheck(qBusySTT,  1) != 'busy') \
                        and (qBusyCheck(qBusyTTS,  1) != 'busy') \
                        and (qBusyCheck(qBusyPlay, 1) != 'busy'):
                            sw = 'on'

                if (sw == 'on'):
                    qBusySet(qBusyInput, True)

                    if (v2w_wave_seq != julius_bakSEQ):
                        julius_bakSEQ = v2w_wave_seq

                    if (adinexe_run == False):
                        adinexe_run = True

                        if (bakSox_run == True):
                            bakSox_run = False
                            if (not bakSox_sbp is None):
                                bakSox_sbp.terminate()
                                bakSox_sbp = None
                            julius_bakLast = ''
                            julius_bakWav  = ''

                        if (micGuide == 'on' or micGuide == 'sound'):
                            qGuide('_ready')

                        if (bakSox_run == False):
                            bakSox_run = True
                            now=datetime.datetime.now()
                            julius_bakLast = qPathInp + now.strftime('%H%M%S') +'.julius.5000.wav'
                            julius_bakWav = qPathWork + 'julius_backup.wav'
                            bakSox_sbp = subprocess.Popen(['sox', '-q', '-d', '-r', '16000', '-b', '16', '-c', '1', \
                                            julius_bakWav, 'trim', '0', '30', ], \
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            #qLogOutput('julius____:backup ' + julius_bakLast)

                        #adinexe_sbp = subprocess.Popen(['adintool', '-in', 'mic', \
                        #    '-rewind', julius_rewind, '-headmargin', julius_headmg, '-tailmargin', julius_tailmg, \
                        #    '-fvad', vadLevel, '-lv', micLevel, \
                        #    '-out', 'adinnet', '-server', 'localhost', '-port', '5530',] , \
                        #    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        #    #stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
                        now=datetime.datetime.now()
                        filename=qPathInp + now.strftime('%H%M%S') +'.julius'
                        adinexe_sbp = subprocess.Popen(['adintool', '-in', 'mic', \
                            '-rewind', julius_rewind, '-headmargin', julius_headmg, '-tailmargin', julius_tailmg, \
                            '-fvad', vadLevel, '-lv', micLevel, \
                            '-out', 'file', '-filename', filename, '-startid', '5001', ] , \
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            #stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )

                    if (os.name == 'nt'):
                      if (adingui_run == False) and (micGuide == 'on' or micGuide == 'display'):
                        adingui_run = True
                        adingui_sbp = subprocess.Popen(['adintool-gui', '-in', 'mic', \
                            '-rewind', julius_rewind, '-headmargin', julius_headmg, '-tailmargin', julius_tailmg, \
                            '-lv', micLevel,] , \
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            #stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )

                sw = 'on'
                if (micType == 'bluetooth') or (micGuide == 'on' or micGuide == 'sound'):
                    if (qBusyCheck(qBusyCtrl, 0) == 'busy') \
                    or (qBusyCheck(qBusySTT,  0) == 'busy') \
                    or (qBusyCheck(qBusyTTS,  0) == 'busy') \
                    or (qBusyCheck(qBusyPlay, 0) == 'busy'):
                        sw = 'off'
                if (adinexe_run == True):
                    files = glob.glob(qPathInp + '*')
                    if (len(files) > 0):
                        chktime = time.time()
                        while (len(files) > 0) and ((time.time() - chktime) < 5):
                            time.sleep(0.20)
                            files = glob.glob(qPathInp + '*')
                        if (len(files) == 0):
                            sw = 'accept'

                if (sw == 'off') or (sw == 'accept'):
                    if (bakSox_run == True):
                        bakSox_run = False
                        if (not bakSox_sbp is None):
                            bakSox_sbp.terminate()
                            bakSox_sbp = None
                        julius_bakLast = ''
                        julius_bakWav  = ''

                    if (adingui_run == True):
                        adingui_run = False
                        if (not adingui_sbp is None):
                            adingui_sbp.terminate()
                            adingui_sbp = None

                    if (adinexe_run == True):
                        adinexe_run = False
                        if (not adinexe_sbp is None):
                            adinexe_sbp.terminate()
                            adinexe_sbp = None

                    qBusySet(qBusyInput, False)

                    if (sw == 'accept'):
                        if (micGuide == 'on' or micGuide == 'sound'):
                             qGuide('_accept')
                             time.sleep(3.00)

                cn_s.put(['OK', ''])

        julius_busy = False

        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.05)

    qLogOutput('julius____:terminate')

    qBusySet(qBusyInput, False)

    if (adingui_run == True):
        adingui_run = False
        if (not adingui_sbp is None):
            adingui_sbp.terminate()
            adingui_sbp = None
    if (adinexe_run == True):
        adinexe_run = False
        if (not adinexe_sbp is None):
            adinexe_sbp.terminate()
            adinexe_sbp = None
    if (adinsvr_run == True):
        adinsvr_run = False
        if (not adinsvr_sbp is None):
            adinsvr_sbp.terminate()
            adinsvr_sbp = None

    qKill('adintool-gui')
    qKill('adintool')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('julius____:end')



def v2w_wave_sub(micDev, seq4, fileId, file, f2, f2size, bytebase, minSize, maxSize, ):
    global qPathCtrl
    global qPathInp
    global qPathWav
    global qPathSTT
    global qPathTTS
    global qPathTRA
    global qPathPlay
    global qPathRec
    global qPathWork

    if (True):

        if (f2size >= int(minSize) and f2size <= int(maxSize+2000)):

                now=datetime.datetime.now()
                stamp=now.strftime('%Y%m%d.%H%M%S')

                if (str(micDev) != 'file'):
                     sec=int((f2size-44)/2/16000)
                else:
                     sec=int(bytebase/2/16000)
                hh=int(sec/3600)
                mm=int((sec-hh*3600)/60)
                ss=int(sec-hh*3600-mm*60)
                tm='{:02}{:02}{:02}'.format(hh,mm,ss)

                f3=qPathWav + stamp + '.' + fileId + '(000).' + tm + '.wav'

                shutil.copy2(f2, f3)

                if (str(micDev) != 'file'):
                    frec=f3.replace(qPathWav, '')
                    frec=qPathRec + frec[:-4] + '.mp3'
                    sox = subprocess.Popen(['sox', '-q', f2, '-r', '16000', '-b', '16', '-c', '1', frec, ], \
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    sox.wait()
                    sox.terminate()
                    sox = None

        if (f2size > int(maxSize+2000)):
            nn=1
            while (nn != 0):

                sepsec=int(maxSize/16000/2 - 1)

                now=datetime.datetime.now()
                stamp=now.strftime('%Y%m%d.%H%M%S')

                f4 = f2[:-4] + '.trim.wav'
                sox = subprocess.Popen(['sox', '-q', f2, '-r', '16000', '-b', '16', '-c', '1', f4, 'trim', str((nn-1)*sepsec), str(sepsec+1), ], \
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

                f4size = 0
                try:
                    rb = open(f4, 'rb')
                    f4size = sys.getsizeof(rb.read())
                    rb.close
                    rb = None
                except:
                    pass

                if (f4size < int(minSize)):
                    nn = 0
                    os.remove(f4)
                else:

                    if (str(micDev) != 'file'):
                        sec=int((f4size-44)/2/16000)
                    else:
                        sec=int(bytebase/2/16000) + (nn-1)*15
                    hh=int(sec/3600)
                    mm=int((sec-hh*3600)/60)
                    ss=int(sec-hh*3600-mm*60)
                    tm='{:02}{:02}{:02}'.format(hh,mm,ss)

                    f5=qPathWav + stamp + '.' + fileId + '(' + '{:03}'.format(nn) + ').' + tm + '.wav'
                    shutil.copy2(f4, f5)

                    if (str(micDev) != 'file'):
                        try:
                            frec=f3.replace(qPathWav, '')
                            frec=qPathRec + frec[:-4] + '.mp3'
                            sox = subprocess.Popen(['sox', '-q', f4, '-r', '16000', '-b', '16', '-c', '1', frec, ], \
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            sox.wait()
                            sox.terminate()
                            sox = None
                        except:
                            pass

                    nn += 1



v2w_wave_start=0
v2w_wave_beat =0
v2w_wave_busy =False
v2w_wave_last =0
v2w_wave_seq  =0

def proc_v2w_wave(cn_r, cn_s, ):
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

    global v2w_wave_start
    global v2w_wave_beat
    global v2w_wave_busy
    global v2w_wave_last
    global v2w_wave_seq

    qLogOutput('v2w_wave__:init')

    runMode  = cn_r.get()
    micDev   = cn_r.get()
    micType  = cn_r.get()
    micGuide = cn_r.get()
    minSize  = cn_r.get()
    maxSize  = cn_r.get()
    cn_r.task_done()

    qLogOutput('v2w_wave__:runMode =' + str(runMode ))
    qLogOutput('v2w_wave__:micDev  =' + str(micDev  ))
    qLogOutput('v2w_wave__:micType =' + str(micType ))
    qLogOutput('v2w_wave__:micGuide=' + str(micGuide))
    qLogOutput('v2w_wave__:minSize =' + str(minSize ))
    qLogOutput('v2w_wave__:maxSize =' + str(maxSize ))

    qLogOutput('v2w_wave__:start')
    v2w_wave_start = time.time()



    while (True):
        v2w_wave_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qLogOutput('v2w_wave__:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qLogOutput('v2w_wave__: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                #v2w_wave_last = time.time()
                cn_s.put(['PASS', ''])

            else:

                v2w_wave_busy = True

                result = 'OK'

                path=qPathInp
                files = glob.glob(path + '*')
                if (len(files) > 0):

                    try:

                        bytebase=0
                        for f in files:
                            file=f.replace('\\', '/')
                            if (os.name != 'nt'):
                                time.sleep(2.00)
                            if (file[-4:].lower() == '.wav' and file[-8:].lower() != '.tmp.wav'):
                                a = open(file, 'a')
                                a.close()
                                a = None
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

                                v2w_wave_seq += 1
                                if (v2w_wave_seq >= 10000):
                                    v2w_wave_seq = 1
                                seq4 = '{:04}'.format(v2w_wave_seq)
                                seq2 = seq4[-2:]

                                wrkfile = qPathWork + 'v2w_wave.' + seq2 + '.wav'
                                if (os.path.exists(wrkfile)):
                                    try:
                                        os.remove(wrkfile)
                                    except:
                                        pass

                                sox = subprocess.Popen(['sox', '-q', file, '-r', '16000', '-b', '16', '-c', '1', wrkfile, ], \
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                                sox.wait()
                                sox.terminate()
                                sox = None

                                if (str(micDev) != 'file'):
                                    os.remove(file)

                                if (os.path.exists(wrkfile)):

                                    if (runMode == 'debug' or str(micDev) == 'file'):
                                        qLogOutput('v2w_wave__:' + fileId + u' → ' + wrkfile[:-4])

                                    wrksize = 0
                                    try:
                                        rb = open(wrkfile, 'rb')
                                        wrksize = sys.getsizeof(rb.read())
                                        rb.close
                                        rb = None
                                    except:
                                        pass

                                    v2w_wave_last = time.time()

                                    v2w_wave_sub(micDev, seq4, fileId, file, wrkfile, wrksize, bytebase, minSize, maxSize,)

                                    if (str(micDev) == 'file'):
                                        bytebase += wrksize - 44

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

        v2w_wave_busy = False

        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.05)

    qLogOutput('v2w_wave__:terminate')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('v2w_wave__:end')



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
        qMakeDirs(qPathInp,  True )
        qMakeDirs(qPathWav,  True )
        qMakeDirs(qPathSTT,  False)
        qMakeDirs(qPathTTS,  False)
        qMakeDirs(qPathTRA,  False)
        qMakeDirs(qPathPlay, False)
        qMakeDirs(qPathRec,  False)
        qMakeDirs(qPathWork, False)
    else:
        qMakeDirs(qPathCtrl, False)
        qMakeDirs(qPathInp,  False)
        qMakeDirs(qPathWav,  True )
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
main_seq  =0
if (__name__ == '__main__'):
    #global main_beat
    #global julius_beat
    #global adinxxx_run
    #global adinxxx_sbp
    #global v2w_wave_beat

    qLogOutput('')
    qLogOutput('v2w_main__:init')
    qLogOutput('v2w_main__:exsample.py runMode, mic..., ')
    #runMode  handsfree, translator, speech, ...,
    #micDev   num or file
    #micType  usb or bluetooth
    #micGuide off, on, display, sound

    runMode  = 'debug'
    micDev   = '0'
    micType  = 'bluetooth'
    micGuide = 'on'
    micLevel = '777'

    minSize  =  10000
    maxSize  = 384000

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        micDev   = str(sys.argv[2]).lower()
        if (str(micDev) == 'file'):
           micGuide = 'off' 
    if (len(sys.argv) >= 4):
        micType  = str(sys.argv[3]).lower()
    if (len(sys.argv) >= 5):
        micGuide = str(sys.argv[4]).lower()
    if (len(sys.argv) >= 6):
        p = str(sys.argv[5]).lower()
        if (p.isdigit() and p != '0'):
            micLevel = p

    qLogOutput('')
    qLogOutput('v2w_main__:runMode  =' + str(runMode  ))
    qLogOutput('v2w_main__:micDev   =' + str(micDev   ))
    qLogOutput('v2w_main__:micType  =' + str(micType  ))
    qLogOutput('v2w_main__:micGuide =' + str(micGuide ))
    qLogOutput('v2w_main__:micLevel =' + str(micLevel ))

    main_init(micDev, )

    qKill('adintool-gui')
    qKill('adintool')

    qLogOutput('')
    qLogOutput('v2w_main__:start')
    main_start     = time.time()
    main_beat      = 0

    julius_s       = queue.Queue()
    julius_r       = queue.Queue()
    julius_proc    = None
    julius_beat    = 0
    julius_pass    = 0

    v2w_wave_s     = queue.Queue()
    v2w_wave_r     = queue.Queue()
    v2w_wave_proc  = None
    v2w_wave_beat  = 0
    v2w_wave_pass  = 0

    while (True):
        main_beat = time.time()

        # check v2w_wave_last

        if (str(micDev) == 'file'):
            if (v2w_wave_last == 0):
                v2w_wave_last = time.time()
            sec = int(time.time() - v2w_wave_last)
            if (sec > 90):
                break

        if (str(micDev) != 'file'):
            if (qBusyCheck(qBusyCtrl, 0) == 'busy' or \
                qBusyCheck(qBusySTT,  0) == 'busy' or \
                qBusyCheck(qBusyTTS,  0) == 'busy' or \
                qBusyCheck(qBusyPlay, 0) == 'busy'):
                v2w_wave_last = 0
            if (v2w_wave_last == 0):
                v2w_wave_last = time.time()
            sec = int(time.time() - v2w_wave_last)
            if (sec > 99): #30->9999->99
                qLogOutput('v2w_main__:julius_proc 99s reboot !')
                julius_beat   = main_start
                v2w_wave_last = 0

        # Thread timeout check

        if (julius_beat != 0):
          if (str(micDev) != 'file'):
            sec = int(time.time() - julius_beat)
            if (sec > 60):
                qLogOutput('v2w_main__:julius_proc 60s')
                qLogOutput('v2w_main__:julius_proc break')
                julius_s.put([None, None])
                time.sleep(3.00)
                julius_proc = None
                julius_beat = 0
                julius_pass = 0

                if (adingui_run == True):
                    adingui_run = False
                    if (not adingui_sbp is None):
                        adingui_sbp.terminate()
                        adingui_sbp = None
                if (adinexe_run == True):
                    adinexe_run = False
                    if (not adinexe_sbp is None):
                        adinexe_sbp.terminate()
                        adinexe_sbp = None
                if (adinsvr_run == True):
                    adinsvr_run = False
                    if (not adinsvr_sbp is None):
                        adinsvr_sbp.terminate()
                        adinsvr_sbp = None

                qKill('adintool-gui')
                qKill('adintool')

                if (micGuide != 'off'):
                    qGuide('_down')

        if (v2w_wave_beat != 0):
          if (str(micDev) != 'file'):
            sec = int(time.time() - v2w_wave_beat)
            if (sec > 60):
                qLogOutput('v2w_main__:v2w_wave_proc 60s')
                qLogOutput('v2w_main__:v2w_wave_proc break')
                v2w_wave_s.put([None, None])
                time.sleep(3.00)
                v2w_wave_proc = None
                v2w_wave_beat = 0
                v2w_wave_pass = 0

        # Thread start

        if (julius_proc is None):
            while (julius_s.qsize() > 0):
                dummy = julius_s.get()
            while (julius_r.qsize() > 0):
                dummy = julius_r.get()
            julius_proc = threading.Thread(target=proc_julius, args=(julius_s,julius_r,))
            julius_proc.daemon = True
            julius_s.put(runMode )
            julius_s.put(micDev  )
            julius_s.put(micType )
            julius_s.put(micGuide)
            julius_s.put(micLevel)
            julius_proc.start()
            time.sleep(1.00)

            julius_s.put(['START', ''])

        if (v2w_wave_proc is None):
            while (v2w_wave_s.qsize() > 0):
                dummy = v2w_wave_s.get()
            while (v2w_wave_r.qsize() > 0):
                dummy = v2w_wave_r.get()
            v2w_wave_proc = threading.Thread(target=proc_v2w_wave, args=(v2w_wave_s,v2w_wave_r,))
            v2w_wave_proc.daemon = True
            v2w_wave_s.put(runMode )
            v2w_wave_s.put(micDev  )
            v2w_wave_s.put(micType )
            v2w_wave_s.put(micGuide)
            v2w_wave_s.put(minSize )
            v2w_wave_s.put(maxSize )
            v2w_wave_proc.start()
            time.sleep(1.00)

            v2w_wave_s.put(['START', ''])

        # processing

        if (julius_r.qsize() == 0 and julius_s.qsize() == 0):
            julius_s.put(['PROC', ''])
            julius_pass += 1
        else:
            julius_pass = 0
        if (julius_pass > 50):
            julius_s.put(['PASS', ''])
            julius_pass = 0

        while (julius_r.qsize() > 0):
            julius_get = julius_r.get()
            julius_res = julius_get[0]
            julius_dat = julius_get[1]
            julius_r.task_done()

        if (v2w_wave_r.qsize() == 0 and v2w_wave_s.qsize() == 0):
            v2w_wave_s.put(['PROC', ''])
            v2w_wave_pass += 1
        else:
            v2w_wave_pass = 0
        if (v2w_wave_pass > 50):
            v2w_wave_s.put(['PASS', ''])
            v2w_wave_pass = 0

        break_flag = False
        while (v2w_wave_r.qsize() > 0):
            v2w_wave_get = v2w_wave_r.get()
            v2w_wave_res = v2w_wave_get[0]
            v2w_wave_dat = v2w_wave_get[1]
            v2w_wave_r.task_done()
            if (v2w_wave_res == 'END'):
                break_flag = True
            if (v2w_wave_res == 'ERROR'):
                break_flag = True
        if (break_flag == True):
            break



        time.sleep(0.05)



    qLogOutput('')
    qLogOutput('v2w_main__:terminate')

    try:
        julius_s.put(  [None, None] )
        v2w_wave_s.put( [None, None] )
        time.sleep(3.00)
    except:
        pass

    if (adingui_run == True):
        adingui_run = False
        if (not adingui_sbp is None):
            adingui_sbp.terminate()
            adingui_sbp = None
    if (adinexe_run == True):
        adinexe_run = False
        if (not adinexe_sbp is None):
            adinexe_sbp.terminate()
            adinexe_sbp = None
    if (adinsvr_run == True):
        adinsvr_run = False
        if (not adinsvr_sbp is None):
            adinsvr_sbp.terminate()
            adinsvr_sbp = None

    qKill('adintool-gui')
    qKill('adintool')

    if (bakSox_run == True):
        bakSox_run = False
        if (not bakSox_sbp is None):
            bakSox_sbp.terminate()
            bakSox_sbp = None

    try:
        julius_proc.join()
        v2w_wave_proc.join()
    except:
        pass

    qBusySet(qBusyInput, False)

    qLogOutput('v2w_main__:bye!')


