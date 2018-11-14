from time import sleep, strftime
import time
import datetime
import telepot
from telepot.loop import MessageLoop
import requests, json

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
        command=msg['text']
        if command == 'hi':
            bot.sendMessage(chat_id, str('Hi '+msg['from']['first_name']+' ' +msg['from']['last_name']))
        if command == 'id':
            file_id = msg['chat']['id']
            print(chat_id)
            bot.sendMessage(chat_id, str(file_id))
       # bot.sendDocument(chat_id, open("/ICON.ICO", 'rb'))
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
