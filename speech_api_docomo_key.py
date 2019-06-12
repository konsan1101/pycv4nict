#!/usr/bin/env python
# -*- coding: utf-8 -*-



def getkey(api,):

    # docomo 音声認識(amivoice)
    if (api == 'stt'):
        return '30323937364562757a48757172664556673133616a6e366446483866676132507771317233686b71694d33'

    # docomo 雑談対話
    if (api == 'chatting'):
        return '746d44434347366243656a6c33363845436f773239704872546f704237415165304b72334c39364f344d42'

    # docomo 知識検索
    if (api == 'knowledge'):
        return '746d44434347366243656a6c33363845436f773239704872546f704237415165304b72334c39364f344d42'

    return False



#  2018/12/20 - 2019/03/07
#  https://dev.smt.docomo.ne.jp/
#  
#  利用状況
#  開発キー （ 利用中 ） 
#  ・「音声認識【Powered by NTTテクノクロス】」 
#  ・「音声認識【Powered by アドバンスト・メディア】」 
#  ・「音声合成【Powered by NTTテクノクロス】」 
#  ・「音声合成【Powerd by エーアイ】」 
#  ・「画像認識」 
#  client id
#  ※【　】 内が値になります。
#  【gruVwQH8Gdh8CHiXhkSeHcS3Y5z4S9U5bMh1pGbYL2zO】
#  client secret
#  ※【　】 内が値になります。
#  【!V4t7Aocp,-#X]^6JRq}】
#  API key
#  ※【　】 内が値になります。
#  【30323937364562757a48757172664556673133616a6e366446483866676132507771317233686b71694d33】
#  

#  2019/01/02 -
#  https://dev.smt.docomo.ne.jp/
#  
#  利用状況 開発キー （ 利用中 ） 
#  ・「自然対話：意図解釈」 
#  ・「自然対話：FAQチャット」 
#  ・「自然対話：雑談対話」 
#  ・「自然対話：知識検索」 
#  ・「自然対話：キャラクタ変換」
#  client id
#  ※【　】 内が値になります。
#  【EGuIiQ9L4PYpNgjgAJWDeNwTQxvRCZr7RreQ2h5T7b8X】
#  client secret
#  ※【　】 内が値になります。
#  【4L\LF^19Bl$7>;];#fR[】
#  API key
#  ※【　】 内が値になります。
#  【746d44434347366243656a6c33363845436f773239704872546f704237415165304b72334c39364f344d42】
#  

