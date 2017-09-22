# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from flask.json import jsonify as flask_jsonify


def jsonify(data, status_code=200):
    res = flask_jsonify(data)
    res.status_code = status_code
    return res

