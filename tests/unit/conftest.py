# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest


@pytest.fixture
def url_for(mocker):
    m = mocker.patch('app.serializers.url_for')
    m.return_value = lambda x, *y, **z: (x, y, z)
    return m

