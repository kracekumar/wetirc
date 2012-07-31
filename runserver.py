#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import os
os.environ['ENVIRONMENT'] = "development"

from wetirc import app
app.run('127.0.0.1', debug=True, port=app.config['WEBAPP_PORTNO'])
