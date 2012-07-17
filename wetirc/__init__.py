#! -*- coding: utf-8 -*-
import logging

from brubeck.connections import Mongrel2Connection
from brubeck.request_handling import Brubeck
from brubeck.templating import load_jinja2_env
from wetirc.views import user

handlers = [
            (r'/$', user.IndexHandler)
            ]

config = {
           'msg_conn': Mongrel2Connection('tcp://127.0.0.1:12344', 'tcp://127.0.0.1:12345'),
           'template_loader': load_jinja2_env('templates'),
           'cookie_secret': 'Damn secret !!!',
           'log_level': logging.DEBUG,
           'handler_tuples': handlers
         }

import os
import sys
sys.path.insert(0, os.getcwd())
print os.getcwd()
app = Brubeck(**config)
