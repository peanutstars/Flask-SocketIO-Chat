#!/usr/bin/env python

import sys
import requests
import json
import time
import logging
import socketio

from bs4 import BeautifulSoup
# from socketIO_client import SocketIO, LoggingNamespace

# logging.basicConfig(
# #   format = '%(asctime)s:%(levelname)s:%(message)s',
# #   datefmt = '%m/%d/%Y %I:%M:%S %p',
#   level = logging.DEBUG
# )


class ChatNamespace(socketio.ClientNamespace):
    def __init__(self, handle, namespace=None):
        super(ChatNamespace, self).__init__(namespace)
        self.handle = handle
        
    def on_connect(self):
        # 서버가 끊어졌다가 다시 연결되는 경우, 로그인이 필요하다.
        self.handle.login()
        self.emit('joined', 'Client joined')
        print('connection established')
    
    def on_disconnect(self):
        print('disconnected')
    
    def on_message(self, data):
        print('message received with ', data['msg'])

class ChatClient:
    HOST_URL = 'http://localhost:5000'
    def __init__(self, name='python', room='room'):
        self.client = requests.Session()
        self.sio = socketio.Client()
        self.name = name
        self.room = room
        self.init()

    def __del__(self):
        self.client.close()

    def init(self):
        self.login()
        self.sio.register_namespace(ChatNamespace(self, '/chat'))
        headers = {'Cookie': f'session={self.client.cookies["session"]}'}
        self.sio.connect(self.HOST_URL, headers=headers, namespaces=['/chat'])
        self.sio.emit('text', {'msg': 'PyClient Message'}, namespace='/chat')

    def login(self):
        r = self.client.get(self.HOST_URL)
        soup = BeautifulSoup(r.text, features="html.parser")
        csrftoken = soup.find('input', dict(name='csrf_token'))['value']
        del soup

        if csrftoken:
            login_data = dict(name=self.name, room=self.room, csrf_token=csrftoken)
            r = self.client.post(self.HOST_URL, data=login_data)
            print(r.status_code, f'with csrf_token: {csrftoken}')

        
    def run(self):
        is_run = True
        while is_run:
            line = input('input:')
            if line.strip() in 'qQ':
                is_run = False
                print('<Quit>')
                continue
            self.sio.emit('text', {'msg': line}, namespace='/chat')

        print("<END>")
        self.sio.disconnect()
        # self.sio.wait()


ChatClient().run()