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
    def on_connect(self):
        self.emit('joined', 'Client joined')
        print('connection established')
    
    def on_disconnect(self):
        print('disconnected')
    
    def on_message(self, data):
        print('message received with', data['msg'])

    def on_status(self, data):
        print('status received with', data['msg'])


class ChatClient:
    HOST_URL = 'http://localhost:5000'
    def __init__(self, name='python', room='room'):
        self.session = requests.Session()
        self.sio = socketio.Client(http_session=self.session)
        print(f'>> Name[{name}], Room[{room}]')
        self.init(name, room)

    def __del__(self):
        self.session.close()

    def init(self, name, room):
        self.login(name, room)
        self.sio.register_namespace(ChatNamespace('/chat'))
        ## socketio.Client() 에서 http_session 파라미터를 통해 session 정보 전달
        # headers = {'Cookie': f'session={self.session.cookies["session"]}'}
        # self.sio.connect(self.HOST_URL, headers=headers, namespaces=['/chat'])
        ## 220509 - Window에서 wait_timeout=1 사용하면, 연결중에 끊기는 문제 발생한다.
        self.sio.connect(self.HOST_URL, wait_timeout=5)
        self.sio.emit('text', {'msg': 'PyClient Message'}, namespace='/chat')

    def login(self, name, room):
        r = self.session.get(self.HOST_URL)
        soup = BeautifulSoup(r.text, features="html.parser")
        csrftoken = soup.find('input', dict(name='csrf_token'))['value']
        del soup

        if csrftoken:
            login_data = dict(name=name, room=room, csrf_token=csrftoken)
            r = self.session.post(self.HOST_URL, data=login_data)
            print(r.status_code, f'with csrf_token: {csrftoken}')

        
    def run(self):
        while True:
            line = input('input:').strip()
            if line and line in 'qQ':
                print('<Quit>')
                break
            if not self.sio.connected:
                print(f'socketio.connected[{self.sio.connected}]')
                break
            self.sio.emit('text', {'msg': line}, namespace='/chat')

        print("<END>")
        self.sio.disconnect()
        # self.sio.wait()


ChatClient().run()