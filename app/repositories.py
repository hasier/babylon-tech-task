# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import ShortURL


logger = logging.getLogger(__name__)


class ShortURLRepository(object):
    @classmethod
    def saveNewURL(cls, url):
        return cls._saveNewURL(url)

    @classmethod
    def _saveNewURL(cls, url, retry=True):
        s = ShortURL(url=url)
        db.session.add(s)
        try:
            db.session.commit()
        except IntegrityError:
            logger.exception('Integrity error storing new shortened URL')
            db.session.rollback()
            if retry:
                db.session.expunge(s)
                s = cls._saveNewURL(url, retry=False)
            else:
                logger.exception('Unrecoverable integrity error storing new shortened URL')
                s = None
        return s

