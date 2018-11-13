from time import sleep, strftime
import time
import datetime
import telepot
from telepot.loop import MessageLoop
import requests, json

import urllib3

from pathlib import Path

proxy_url = "http://94.243.140.162:40960"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=80),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))



print(strftime('%H:%M:%S'))


def handle(msg):
    chat_id=msg['chat']['id']
    command=msg['text']

    print('Recieved: ')
    print(command)

    if command == 'hi':
        bot.sendMessage(chat_id, str('Hi'))
        

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
