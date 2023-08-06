SECRET_KEY = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

INSTALLED_APPS = ("django.contrib.auth", "django.contrib.contenttypes", "cool_django_auth_ldap", "tests")

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "dev.db"}}

AUTHENTICATION_BACKENDS = ["cool_django_auth_ldap.backend.LDAPBackend"]
