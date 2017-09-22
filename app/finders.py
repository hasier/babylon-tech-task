# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from app import db
from app.models import ShortURL


class ShortURLFinder(object):
    @classmethod
    def getURLFromShort(cls, shortened_url):
        return db.session.query(ShortURL).filter(ShortURL.shortened_url == shortened_url).first()

