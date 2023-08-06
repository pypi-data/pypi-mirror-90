==================
wca-django-allauth
==================

`World Cube Association <https://www.worldcubeassociation.org/>`__ OAuth2 provider for
`django-allauth <https://django-allauth.readthedocs.io/en/latest/overview.html>`__.

Installation
============

Install the package

::

    $ pip install wca-django-allauth

settings.py

::

    INSTALLED_APPS = [
        # ... django and allauth apps

        'wca_allauth',
    ]

Callback URL

::

    http://example.com/accounts/worldcubeassociation/login/callback/

Login URL

::

    http://example.com/accounts/worldcubeassociation/login

