=====
Usage
=====

To use the auth backend in a Django project, add
``'cool_django_auth_ldap.backend.LDAPBackend'`` to
:setting:`AUTHENTICATION_BACKENDS`m add ``cool_django_auth_ldap`` to
:setting:`INSTALLED_APPS` and run migrations.

.. code-block:: python

    AUTHENTICATION_BACKENDS = ["cool_django_auth_ldap.backend.LDAPBackend"]

    INSTALLED_APPS = (
        ...
        "cool_django_auth_ldap.apps.AppConfig"
        ...
    )

:class:`~cool_django_auth_ldap.backend.LDAPBackend` should work with custom user
models, but it does assume that a database is present.

.. note::

    :class:`~cool_django_auth_ldap.backend.LDAPBackend` does not inherit from
    :class:`~django.contrib.auth.backends.ModelBackend`. It is possible to use
    :class:`~cool_django_auth_ldap.backend.LDAPBackend` exclusively by configuring
    it to draw group membership from the LDAP server. However, if you would
    like to assign permissions to individual users or add users to groups
    within Django, you'll need to have both backends installed:

    .. code-block:: python

        AUTHENTICATION_BACKENDS = [
            "cool_django_auth_ldap.backend.LDAPBackend",
            "django.contrib.auth.backends.ModelBackend",
        ]
