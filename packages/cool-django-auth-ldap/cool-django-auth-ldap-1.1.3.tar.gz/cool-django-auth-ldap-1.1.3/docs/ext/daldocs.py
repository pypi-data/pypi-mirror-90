"""
Extra stuff for the cool-django-auth-ldap Sphinx docs.
"""


def setup(app):
    app.add_crossref_type(
        directivename="setting", rolename="setting", indextemplate="pair: %s; setting"
    )
