#! -*- coding: utf-8 -*-

from flask import Flask
from coaster import configureapp

app = Flask('wetirc', instance_relative_config=True)
configureapp(app, 'ENVIRONMENT')

# setting here path
import os
import sys

path = os.path.dirname(__file__)
sys.path.insert(0, path)

import wetirc.views
