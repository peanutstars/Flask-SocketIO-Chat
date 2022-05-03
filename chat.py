#!/bin/env python

import logging

from app import create_app, socketio


logging.basicConfig(
#   format = '%(asctime)s:%(levelname)s:%(message)s',
#   datefmt = '%m/%d/%Y %I:%M:%S %p',
  level = logging.DEBUG
)

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
