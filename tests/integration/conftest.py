# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest

from alembic.command import downgrade, upgrade
from alembic.config import Config


@pytest.fixture(scope='session')
def app():
    from app import app
    return app


@pytest.fixture
def with_app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def database(app, request):
    from app import db
    config = Config('alembic.ini')
    downgrade(config, 'base')
    upgrade(config, 'head')

    def downgrade_db():
        db.session.remove()
        downgrade(config, 'base')

    request.addfinalizer(downgrade_db)
    return db

@pytest.fixture
def api_client(app):
    test_client = app.test_client()
    return test_client

