# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from urlparse import urlparse

from app.models import ShortURL


def test_get_shortened_fail(api_client, database):
    response = api_client.get('/asdf')
    assert response.status_code == 404


def test_get_shortened(api_client, with_app_context, database):
    url = 'http://www.google.com'
    s = ShortURL(url=url)
    database.session.add(s)
    database.session.commit()

    response = api_client.get('/{}'.format(s.shortened_url))
    assert response.status_code == 302
    assert response.headers.get('Location') == url

def test_shorten_no_body(api_client, database):
    response = api_client.post('/shorten_url')
    assert response.status_code == 400
    assert json.loads(response.data).get('key') == 'client_error'

def test_shorten_malformed(api_client, database):
    response = api_client.post('/shorten_url', data=json.dumps(dict(url='asdf')))
    assert response.status_code == 400
    assert json.loads(response.data).get('key') == 'malformed_url'

def test_shorten(api_client, with_app_context, database):
    url = 'http://www.google.com'
    response = api_client.post('/shorten_url', data=json.dumps(dict(url=url)))
    assert response.status_code == 201
    body = json.loads(response.data)
    assert 'shortened_url' in body
    path = urlparse(body['shortened_url']).path
    s = database.session.query(ShortURL).filter(ShortURL.shortened_url == path[1:]).first()
    assert s is not None
    assert s.url == url

