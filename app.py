#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import logging
import sys
import os

from brubeck.connections import Mongrel2Connection
from brubeck.request_handling import Brubeck
from brubeck.templating import load_jinja2_env
from wetirc.views.user import *
from settings import CHANNELS
#sys.path.insert(0, os.path.dirname(os.getcwd()))

handlers = [
            (r'/channel/(\b)$/', IRCChannel),
            (r'/$', IndexHandler)
            ]
#App configuration
config = {
           'msg_conn': Mongrel2Connection('tcp://127.0.0.1:12344', 'tcp://127.0.0.1:12345'),
           'template_loader': load_jinja2_env('wetirc/templates'),
           'cookie_secret': 'Damn secret !!!',
           'log_level': logging.DEBUG,
           'handler_tuples': handlers
         }
app = Brubeck(**config)
app.__dict__['channels'] = CHANNELS
app.run()