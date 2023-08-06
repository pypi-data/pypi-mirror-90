# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Esteban J. Garcia Gabancho.
# Copyright (C) 2020 Mojib Wali.
#
# invenio-shibboleth is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""
from __future__ import absolute_import, print_function

from flask import Flask

from invenio_shibboleth import Invenioshibboleth


def test_version():
    """Test version import."""
    from invenio_shibboleth import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = Invenioshibboleth(app)
    assert "invenio-shibboleth" in app.extensions

    app = Flask("testapp")
    ext = Invenioshibboleth()
    assert "invenio-shibboleth" not in app.extensions
    ext.init_app(app)
    assert "invenio-shibboleth" in app.extensions
