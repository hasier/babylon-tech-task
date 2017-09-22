# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from flask import url_for


class ShortURLSerializer(object):
    @classmethod
    def serialize(cls, short_url):
        if not short_url:
            return None
        return dict(shortened_url=url_for('get_shortened', path=short_url.shortened_url, _external=True))

