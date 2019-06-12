#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs
import subprocess

import requests
import json



# weather 天気予報
import speech_api_weather_key as weather_key



class WeatherAPI:

    def __init__(self, ):
        self.timeOut   = 10

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def getWeather(self, api, key, city, ):
        weather  = ''
        temp_max = ''
        temp_min = ''
        humidity = ''

        # openweathermap
        if (api == 'openweathermap'):
                url  = 'http://api.openweathermap.org/data/2.5/weather'
                params = {
                    'q': city.replace(' ', ''),
                    'units': 'metric',
                    'lang': 'ja',
                    'mode': 'json',
                    'appid':  key,
                    }
                try:
                    res = requests.post(url, params=params, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        res_json = res.json()
                        #print(res_json)
                        weather  = str(res_json['weather'][0]['description'])
                        temp_max = str(res_json['main']['temp_max'])
                        temp_min = str(res_json['main']['temp_min'])
                        humidity = str(res_json['main']['humidity'])
                except:
                    pass

        return weather, temp_max, temp_min, humidity



if __name__ == '__main__':

        #tenkiAPI = weather_api.WeatherAPI()
        tenkiAPI = WeatherAPI()

        city = u'三木市'

        api = 'openweathermap'
        key = weather_key.getkey(api)
        weather, temp_max, temp_min, humidity = \
            tenkiAPI.getWeather(api, key, city, )

        print(city + u'、今日の天気は、「' + weather + u'」です。')
        print(u'最高気温は、' + temp_max + u'℃。')
        print(u'最低気温は、' + temp_min + u'℃。')
        print(u'湿度は、' + humidity + u'%です。')



