"""
cool_django_auth_ldap AppConfig
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfig):
    name = 'cool_django_auth_ldap'
    verbose_name = _('Cool Django Auth Ldap')
