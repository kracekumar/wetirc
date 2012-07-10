#! /usr/bin/env python
#! -*- coding: utf-8 -*-

from brubeck.connections import Mongrel2Connection
from brubeck.request_handling import Brubeck
from brubeck.templating import load_jinja2_env

import logging
import sys
import os
from wetirc.views.user import *
#sys.path.insert(0, os.path.dirname(os.getcwd()))

#App configuration
config = {
           'msg_conn': Mongrel2Connection('tcp://127.0.0.1:12344', 'tcp://127.0.0.1:12345'),
           'template_loader': load_jinja2_env('wetirc/templates'),
           'cookie_secret': 'Damn secret !!!',
           'log_level': logging.DEBUG,
           'handler_tuples': [(r'^/', IndexHandler)]
         }
app = Brubeck(**config)
app.run()