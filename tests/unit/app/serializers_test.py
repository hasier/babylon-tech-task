# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from app.models import ShortURL
from app.serializers import ShortURLSerializer

class TestShortURLSerializer(object):
    @staticmethod
    def test_serialize_none():
        assert ShortURLSerializer.serialize(None) == None

    @staticmethod
    def test_serialize(url_for):
        url = 'http://www.google.com'
        shortened_url = 'sd75UY'
        s = ShortURL(url=url, shortened_url=shortened_url)
        result = ShortURLSerializer.serialize(s)
        list_keys = ['shortened_url']
        assert len(list_keys) == len(result)
        assert all(key in result for key in list_keys)

