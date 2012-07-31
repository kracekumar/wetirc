#! -*- coding: utf-8 -*-

from flask import Flask


app = Flask('wetirc', instance_relative_config=True)
app.config.from_pyfile('settings.py')
#configureapp(app, 'ENVIRONMENT')

# setting here path
import os
import sys

path = os.path.dirname(__file__)
sys.path.insert(0, path)

import wetirc.views
