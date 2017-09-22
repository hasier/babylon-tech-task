# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging.config
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.errors import setup_errors

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)
setup_errors(app)

logging_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(logging_config, disable_existing_loggers=False)

from app import api, models

