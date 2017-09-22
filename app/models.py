# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from app import db


class ShortURL(db.Model):
    __tablename__ = 'short_url'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    shortened_url = db.Column(db.Text, index=True, unique=True)

