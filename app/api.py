# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from flask import redirect, request
from validators.url import url

from app import app
from app.errors import ClientError, CoreError, NotFoundError
from app.finders import ShortURLFinder
from app.repositories import ShortURLRepository
from app.serializers import ShortURLSerializer
from app.utils import jsonify


@app.route('/<path>', methods=['GET'])
def get_shortened(path):
    short_url = ShortURLFinder.get_url_from_short(path)
    if not short_url:
        raise NotFoundError('Short URL not found')
    return redirect(short_url.url)


@app.route('/shorten_url', methods=['POST'])
def shorten():
    req = request.get_json(force=True)
    if 'url' not in req:
        raise ClientError('Missing URL parameter')

    if not url(req['url'], public=True):
        raise ClientError('Invalid URL', 'malformed_url')

    short_url = ShortURLRepository.save_new_url(req['url'])
    if not short_url:
        raise CoreError(500, 'Could not shorten the URL, please try again', 'unexpected_server_error')
    return jsonify(ShortURLSerializer.serialize(short_url), status_code=201)

