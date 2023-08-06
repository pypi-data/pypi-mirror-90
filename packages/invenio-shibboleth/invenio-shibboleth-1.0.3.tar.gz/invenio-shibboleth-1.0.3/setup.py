# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 TU Graz.
#
# invenio-shibboleth is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module module that provides SAML integration."""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = [
    "pytest-invenio>=1.4.1",
    "invenio-app>=1.0.4",
    "invenio-mail>=1.0.0",
    "invenio-userprofiles>=1.0.0",
    "redis>=2.10.5",
    "mock>=2.0.0",
    "psycopg2-binary>=2.8.6",
]

extras_require = {
    "docs": [
        "Sphinx>=3",
    ],
    "mysql": [
        "invenio-db[mysql]>=1.0.0",
    ],
    "postgresql": [
        "invenio-db[postgresql]>=1.0.0",
    ],
    "sqlite": [
        "invenio-db>=1.0.0",
    ],
    "tests": tests_require,
}

extras_require["all"] = []
for reqs in extras_require.values():
    extras_require["all"].extend(reqs)

setup_requires = [
    "Babel>=1.3",
    "pytest-runner>=3.0.0,<5",
]

install_requires = [
    "python3-saml>=1.5.0",
    "invenio_oauthclient>=1.4.1",
    "invenio-app>=1.3.0",
    "invenio-accounts>=1.4.0",
    "idna>=2.5,<3",
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("invenio_shibboleth", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="invenio-shibboleth",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords="invenio TODO",
    license="MIT",
    author="Mojib Wali",
    author_email="mb_wali@hotmail.com",
    url="https://github.com/tu-graz-library/invenio-shibboleth",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "invenio_base.apps": [
            "invenio_shibboleth = invenio_shibboleth:Invenioshibboleth",
        ],
        "invenio_base.api_apps": [
            "invenio_shibboleth = invenio_shibboleth:Invenioshibboleth",
        ],
        "invenio_i18n.translations": [
            "messages = invenio_shibboleth",
        ],
        "invenio_db.models": [
            "invenio_shibboleth = invenio_shibboleth.invenio_accounts.models",
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
    ],
)
