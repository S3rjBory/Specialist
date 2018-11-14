from time import sleep, strftime
import time
import datetime
import telepot
from telepot.loop import MessageLoop
import requests, json
from weather import Weather, Unit
import urllib3
from pathlib import Path
import os

proxy_url = "http://94.243.140.162:40960"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=80),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

print(strftime('%H:%M:%S'))

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    
    chat_id=msg['chat']['id']
    #command=msg['text']

    content_type, chat_type, chat_id = telepot.glance(msg,'chat')
    chat_idint=str(chat_id)
    print(chat_idint)

    print('Recieved: ')
    #print(command)

    if content_type == 'text':
        command = msg['text']
        words = command.split(' ')
        
        if len(words) >= 2:
            first_word = words[0]
            second_word = words[1]
            print(first_word)
            print(second_word)
        else:
            first_word = 'None'
            second_word = 'None'
        
        if command == 'hi':
            bot.sendMessage(chat_id, str('Hi '+msg['from']['first_name']+' ' +msg['from']['last_name']))
        
        if command == 'id':
            file_id = msg['chat']['id']
            print(chat_id)
            bot.sendMessage(chat_id, str(file_id))
                                                           # bot.sendDocument(chat_id, open("/ICON.ICO", 'rb'))
        if command == 'pogoda':
            a = pogoda()
            bot.sendMessage(chat_id, str(a))

        if (first_word == 'download')&(second_word =='doc'):
            d = words[2]
            bot.sendDocument(chat_id, open('C:/tmp/'+chat_idint+'/doc/'+d, 'rb'))

        if (first_word == 'ls')&(second_word == 'doc'):
            ls = os.listdir('C:/tmp/'+chat_idint+'/doc')
            print(ls)
            bot.sendMessage(chat_id, str(ls))

        if (first_word == 'download')&(second_word =='img'):
            d = words[2]
            bot.sendPhoto(chat_id, open('C:/tmp/'+chat_idint+'/img/'+d+'.png', 'rb'))  # доработать этот блок норм. С выбором по номеру картинку, например

        if (first_word == 'ls')&(second_word == 'img'):
            ls = os.listdir('C:/tmp/'+chat_idint+'/img')
            print(ls)
            bot.sendMessage(chat_id, str(ls))

    if content_type == 'photo':
        print(msg)
        
        try:
            os.mkdir('C:/tmp/'+chat_idint+'/img', mode=0o777)
        except OSError as error:
            print(error)
        try:
            bot.download_file(msg['photo'][-1]['file_id'], 'C:/tmp/'+chat_idint+'/img/'+msg['photo'][-1]['file_id']+'.png')
            bot.sendMessage(chat_id, str(msg['photo'][-3]['file_id']))
   
        except Exception as e:
            bot.sendMessage(chat_id, str('No'))
            print(e)

    if content_type == 'document':
        print(msg['document']['file_name'])
        try:
            os.mkdir('C:/tmp/'+chat_idint+'/doc', mode=0o777)
        except OSError as error:
            print(error)
        try:
            bot.download_file(msg['document']['file_id'], 'C:/tmp/'+chat_idint+'/doc/'+msg['document']['file_name'])
            bot.sendMessage(chat_id, str(msg['document']['file_name']))
   
        except Exception as e:
            bot.sendMessage(chat_id, str('No'))
            bot.sendMessage(chat_id, str(e))
            print(e)

def pogoda():
    weather = Weather(unit=Unit.CELSIUS)

    location = weather.lookup_by_location('moscow')
    forecasts = location.forecast
    n = 0
    for forecast in forecasts:
        while n < 1:
           pogoda_last = [forecast.text, forecast.date, forecast.high]
           n+=1
    return pogoda_last

bot=telepot.Bot('522725344:AAGyVp0GjWPzYvW_BKaL3qBEj-ibOiXxwWY') #@RaspberrySerjTestBot
print(bot.getMe())

MessageLoop(bot, handle).run_as_thread()
print("Listening...")

try:
    while True:
        sleep(1)
        print('Time is: '+strftime('%H:%M:%S'))
except KeyboardInterrupt:
    pass
