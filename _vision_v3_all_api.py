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



#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)



qApiCV     = 'google'
qApiOCR    = qApiCV
qApiTrn    = qApiCV
qLangCV    = 'ja'
qLangOCR   = qLangCV
qLangTrn   = 'en'

qPathDetect= 'temp/v3_1detect/'
qPathPhoto = 'temp/v3_2photo/'
qPathCv    = 'temp/v3_3cv_txt/'
qPathRec   = 'temp/v3_8recorder/'
qPathWork  = 'temp/v3_9work/'

qPathTTS   = 'temp/a3_5tts_txt/'

qCtrlResultCV  = 'temp/temp_resultCV.txt'
qCtrlResultOCR = 'temp/temp_resultOCR.txt'
qCtrlResultTrn = 'temp/temp_resultTrn.txt'



# google 画像認識、OCR認識
import vision_api_google     as google_api
import vision_api_google_key as google_key

# google 機械翻訳
import speech_api_google     as a_google_api
import speech_api_google_key as a_google_key

# azure 画像認識、OCR認識
import vision_api_azure     as azure_api
import vision_api_azure_key as azure_key

# azure 翻訳機能
import speech_api_azure     as a_azure_api
import speech_api_azure_key as a_azure_key



def qVisionCV(useApi='google', inpLang='ja', inpFile='vision__cv_photo.jpg', tmpFile='temp_cv_photo.jpg', apiRecovery=False,):
    resText = ''
    resApi  = ''
    resAry  = None
    resLM   = ''

    api   = useApi
    if  (api != 'free') and (api != 'google') \
    and (api != 'azure'):
        api = 'google'

    if (resText == '') and (api == 'azure'):
        azureAPI = azure_api.VisionAPI()
        res = azureAPI.authenticate('cv' ,
                   azure_key.getkey('cv' ,'url'),
                   azure_key.getkey('cv' ,'key'), )
        if (res == True):
            res = azureAPI.convert(inpImage=inpFile, outImage=tmpFile, bw=False, )
            if (res == True):
                res, api = azureAPI.cv(inpImage=tmpFile, inpLang=inpLang, )
                if (not res is None):
                    #print(res)
                    if (res['captions'] != ''):
                        resText = res['captions']
                        resLM   = resText
                    else:
                        resText = res['categories']
                    resApi  = api
                    resAry  = []
                    if (res['captions'] != ''):
                        resAry.append('[captions] ' + inpLang + ' (' + api + ')')
                        resAry.append(' ' + res['captions'])
                        resAry.append('')
                    if (res['categories'] != ''):
                        resAry.append('[categories] ' + inpLang + ' (' + api + ')')
                        resAry.append(' ' + res['categories'])
                        resAry.append('')
                    if (res['description'] != ''):
                        resAry.append('[description] ' + inpLang + ' (' + api + ')')
                        resAry.append(' ' + res['description'])
                        resAry.append('')

        if (resText == '') and (apiRecovery == True):
            api   = 'free'

    if (resText == '') and ((api == 'free') or (api == 'google')):
        googleAPI = google_api.VisionAPI()
        res = googleAPI.authenticate('cv' ,
                   google_key.getkey('cv' ,'url'),
                   google_key.getkey('cv' ,'key'), )
        if (res == True):
            res = googleAPI.convert(inpImage=inpFile, outImage=tmpFile, bw=False, )
            if (res == True):
                res, api = googleAPI.cv(inpImage=tmpFile, inpLang=inpLang, )
                if (not res is None):
                    #print(res)
                    if (res['landmark'] != ''):
                        resText = res['landmark']
                        resLM   = resText
                    else:
                        resText = res['label']
                    resApi  = api
                    resAry  = []
                    if (res['landmark'] != ''):
                        resAry.append('[landmark] ' + inpLang + ' (' + api + ')')
                        resAry.append(' ' + res['landmark'])
                        resAry.append('')
                    if (res['label'] != ''):
                        resAry.append('[label] ' + inpLang + ' (' + api + ')')
                        resAry.append(' ' + res['label'])
                        resAry.append('')

    if (resText != ''):
        return resText, resApi, resAry, resLM

    return '', '', None, ''



def qVisionOCR(useApi='google', inpLang='ja', inpFile='vision__ocr_photo.jpg', tmpFile='temp_ocr_photo.jpg', apiRecovery=False,):
    resText = ''
    resApi  = ''
    resAry  = None

    api   = useApi
    if  (api != 'free') and (api != 'google') \
    and (api != 'azure'):
        api = 'google'

    if (resText == '') and (api == 'azure'):
        azureAPI = azure_api.VisionAPI()
        res = azureAPI.authenticate('ocr' ,
                   azure_key.getkey('ocr' ,'url'),
                   azure_key.getkey('ocr' ,'key'), )
        if (res == True):
            res = azureAPI.convert(inpImage=inpFile, outImage=tmpFile, bw=True, )
            if (res == True):
                res, api = azureAPI.ocr(inpImage=tmpFile, inpLang=inpLang, )
                if (not res is None):
                    #print(res)
                    resText = ''
                    resApi  = api
                    resAry  = []
                    if (len(res) > 0):
                        resAry.append('[OCR] ' + inpLang + ' (' + api + ')')
                        for text in res:
                            resAry.append(' ' + text)
                            resText += ' ' + text
                            resText = str(resText).strip()

    if (resText == '') and ((api == 'free') or (api == 'google')):
        googleAPI = google_api.VisionAPI()
        res = googleAPI.authenticate('ocr' ,
                   google_key.getkey('ocr' ,'url'),
                   google_key.getkey('ocr' ,'key'), )
        if (res == True):
            res = googleAPI.convert(inpImage=inpFile, outImage=tmpFile, bw=True, )
            if (res == True):
                res, api = googleAPI.ocr(inpImage=tmpFile, inpLang=inpLang, )
                if (not res is None):
                    #print(res)
                    resText = ''
                    resApi  = api
                    resAry  = []
                    if (len(res) > 0):
                        resAry.append('[OCR] ' + inpLang + ' (' + api + ')')
                        for text in res:
                            resAry.append(' ' + text)
                            resText += ' ' + text
                            resText = str(resText).strip()

    if (resText != ''):
        return resText, resApi, resAry

    return '', '', None



def qOCR2Trn(useApi='google', inpLang='ja', inpAry=['Hallo'], trnLang='en', apiRecovery=False,):
    resText = ''
    resApi  = ''
    resAry  = None

    api   = useApi
    if  (api != 'free') and (api != 'google') \
    and (api != 'azure'):
        api = 'google'

    if (resText == '') and (api == 'azure'):
        a_azureAPI = a_azure_api.SpeechAPI()
        ver, key = a_azure_key.getkey('tra')
        res = a_azureAPI.authenticate('tra', ver, key, )
        if (a_res == True):
            resAry = []
            resAry.append('[Translate] ' + trnLang + ' (' + api + ')')
            l = 0
            for text in inpAry:
                l+=1
                if ( l>1 ):
                    outText, api = a_azureAPI.translate(inpText=text, inpLang=inpLang, outLang=trnLang, )
                    if (outText != ''):
                        text   = outText
                        resApi = api
                    resAry.append(text)
                    resText += str(text) + ','

    if (resText == '') and ((api == 'free') or (api == 'google')):
        a_googleAPI = a_google_api.SpeechAPI()
        a_res = a_googleAPI.authenticate('tra', a_google_key.getkey('tra'), )
        if (a_res == True):
            resAry = []
            resAry.append('[Translate] ' + trnLang + ' (' + api + ')')
            l = 0
            for text in inpAry:
                l+=1
                if ( l>1 ):
                    outText, api = a_googleAPI.translate(inpText=text, inpLang=inpLang, outLang=trnLang, )
                    if (outText != ''):
                        text   = outText
                        resApi = api
                    resAry.append(text)
                    resText += str(text) + ','

    if (resText != ''):
        return resText, resApi, resAry

    return '', '', None



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

if (__name__ == '__main__'):
    qMakeDirs('temp/_log/',   False)

    qLogOutput('___main___:init')

    qLogOutput('___main___:exsample.py runMode, api..., lang..., etc..., ')
    #runMode  debug, ...
    #api      google, azure,
    #lang     ja, en, fr, kr...

    runMode  = 'debug'
    camDev   = '0'

    procId   = '00'
    fileId   = 'temp_sample'

    inpCV    = 'vision__cv_photo.jpg'
    tmpCV    = 'temp_cv_photo.jpg'
    outCV    = 'temp_cv_ja.txt'
    inpOCR   = 'vision__ocr_photo.jpg'
    tmpOCR   = 'temp_ocr_photo.jpg'
    outOCR   = 'temp_ocr_ja.txt'
    outTrn   = 'temp_ocr_en.txt'

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        camDev   = str(sys.argv[2]).lower()
    if (len(sys.argv) >= 4):
        qApiCV   = str(sys.argv[3]).lower()
        qApiOCR  = qApiCV
        qApiTrn  = qApiCV
    if (len(sys.argv) >= 5):
        qApiOCR  = str(sys.argv[4]).lower()
    if (len(sys.argv) >= 6):
        qApiTrn  = str(sys.argv[5]).lower()
    if (len(sys.argv) >= 7):
        qLangCV  = str(sys.argv[6]).lower()
        qLangOCR = qLangCV
    if (len(sys.argv) >= 8):
        qLangOCR = str(sys.argv[7]).lower()
    if (len(sys.argv) >= 9):
        qLangTrn = str(sys.argv[8]).lower()

    if (len(sys.argv) >= 10):
        procId   = sys.argv[9]
    if (len(sys.argv) >= 11):
        fileId   = sys.argv[10]

    if (len(sys.argv) >= 12):
        inpCV = sys.argv[11]
    if (len(sys.argv) >= 13):
        tmpCV = sys.argv[12]
    if (len(sys.argv) >= 14):
        outCV = sys.argv[13]
    if (len(sys.argv) >= 15):
        inpOCR = sys.argv[14]
    if (len(sys.argv) >= 16):
        tmpOCR = sys.argv[15]
    if (len(sys.argv) >= 17):
        outOCR = sys.argv[16]
    if (len(sys.argv) >= 18):
        outTrn = sys.argv[17]

    qLogOutput('')
    qLogOutput('___main___:runMode  =' + str(runMode  ))
    qLogOutput('___main___:camDev   =' + str(camDev   ))
    qLogOutput('___main___:qApiCV   =' + str(qApiCV   ))
    qLogOutput('___main___:qApiOCR  =' + str(qApiOCR  ))
    qLogOutput('___main___:qApiTrn  =' + str(qApiTrn  ))
    qLogOutput('___main___:qLangCV  =' + str(qLangCV  ))
    qLogOutput('___main___:qLangOCR =' + str(qLangOCR ))
    qLogOutput('___main___:qLangTrn =' + str(qLangTrn ))

    qLogOutput('___main___:procId   =' + str(procId   ))
    qLogOutput('___main___:fileId   =' + str(fileId   ))

    qLogOutput('___main___:inpCV    =' + str(inpCV    ))
    qLogOutput('___main___:tmpCV    =' + str(tmpCV    ))
    qLogOutput('___main___:outCV    =' + str(outCV    ))
    qLogOutput('___main___:inpOCR   =' + str(inpOCR   ))
    qLogOutput('___main___:tmpOCR   =' + str(tmpOCR   ))
    qLogOutput('___main___:outOCR   =' + str(outOCR   ))
    qLogOutput('___main___:outTrn   =' + str(outTrn   ))



    qLogOutput('')
    qLogOutput('___main___:start')



    if (inpCV != ''):
        res,api,ary,landmark = qVisionCV(qApiCV, qLangCV, inpCV, tmpCV)
        if (api == qApiCV) or (api == 'free' and qApiCV == 'google'):
                qLogOutput(' ' + procId + ' Vision CV    [' + res + '] ' + qLangCV + ' (' + api + ')', True)
        else:
            if (api != ''):
                qLogOutput(' ' + procId + ' Vision CV    [' + res + '] ' + qLangCV + ' (!' + api + ')', True)
            else:
                qLogOutput(' ' + procId + ' Vision CV    [' + res + '] ' + qLangCV + ' (!' + qApiCV + ')', True)

        if (res != ''):
            if (outCV != ''):
                try:
                    w = codecs.open(outCV, 'w', 'utf-8')
                    for text in ary:
                        w.write(str(text) + '\n')
                        #qLogOutput(str(text), True)
                    w.close()
                    w = None
                except:
                    pass

            if (qCtrlResultCV != ''):
                try:
                    w = codecs.open(qCtrlResultCV, 'w', 'utf-8')
                    for text in ary:
                        w.write(str(text) + '\n')
                    w.close()
                    w = None
                except:
                    pass

            if (landmark != ''):
                qLogOutput(' ' + procId + ' Landmark     [' + landmark + '] ' + qLangCV + ' (!' + qApiCV + ')', True)

                recfile = outCV.replace(qPathCv, '')
                recfile = recfile.replace(qPathRec, '')
                recfile = qPathTTS + recfile
                try:
                    w = codecs.open(recfile, 'w', 'utf-8')
                    w.write(landmark)
                    w.close()
                    w = None
                except:
                    w = None



    if (inpOCR != ''):
        res,api,ary = qVisionOCR(qApiOCR, qLangOCR, inpOCR, tmpOCR)
        if (api == qApiOCR) or (api == 'free' and qApiOCR == 'google'):
                qLogOutput(' ' + procId + ' Vision OCR   [' + res + '] ' + qLangOCR + ' (' + api + ')', True)
        else:
            if (api != ''):
                qLogOutput(' ' + procId + ' Vision OCR   [' + res + '] ' + qLangOCR + ' (!' + api + ')', True)
            else:
                qLogOutput(' ' + procId + ' Vision OCR   [' + res + '] ' + qLangOCR + ' (!' + qApiOCR + ')', True)

        if (res != ''):
            if (outOCR != ''):
                try:
                    w = codecs.open(outOCR, 'w', 'utf-8')
                    for text in ary:
                        w.write(str(text) + '\n')
                        #qLogOutput(str(text), True)
                    w.close()
                    w = None
                except:
                    pass

            if (qCtrlResultOCR != ''):
                try:
                    w = codecs.open(qCtrlResultOCR, 'w', 'utf-8')
                    for text in ary:
                        w.write(str(text) + '\n')
                    w.close()
                    w = None
                except:
                    pass

            trnRes,trnApi,trnAry = qOCR2Trn(qApiTrn, qLangOCR, ary, qLangTrn)
            if (api == qApiOCR) or (api == 'free' and qApiOCR == 'google'):
                    qLogOutput(' ' + procId + ' Vision Trns  [' + trnRes + '] ' + qLangTrn + ' (' + api + ')', True)
            else:
                if (api != ''):
                    qLogOutput(' ' + procId + ' Vision Trans [' + trnRes + '] ' + qLangTrn + ' (!' + api + ')', True)
                else:
                    qLogOutput(' ' + procId + ' Vision Trans [' + trnRes + '] ' + qLangTrn + ' (!' + qApiTrn + ')', True)

            if (trnRes != ''):
                if (outTrn != ''):
                    try:
                        w = codecs.open(outTrn, 'w', 'utf-8')
                        for text in trnAry:
                            w.write(str(text) + '\n')
                            #qLogOutput(str(text), True)
                        w.close()
                        w = None
                    except:
                        pass

                if (qCtrlResultTrn != ''):
                    try:
                        w = codecs.open(qCtrlResultTrn, 'w', 'utf-8')
                        for text in trnAry:
                            w.write(str(text) + '\n')
                        w.close()
                        w = None
                    except:
                        pass



    qLogOutput('___main___:terminate')

    qLogOutput('___main___:bye!')



