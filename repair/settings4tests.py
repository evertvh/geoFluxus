"""
Django settings for repair project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from repair.settings import *
import sys

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': 'db_tests.sqlite3',
    },

}

if sys.platform == 'linux':
    SPATIALITE_LIBRARY_PATH = 'mod_spatialite.so'
else:
    SPATIALITE_LIBRARY_PATH = 'mod_spatialite'

MIGRATION_MODULES = {
    #'auth': None,
    #'contenttypes': None,
    #'default': None,
    #'sessions': None,

    #'login': None,
    #'asmfa': None,
    #'studyarea': None,
    #'changes': None,
    #'profiles': None,
    #'snippets': None,
    #'scaffold_templates': None,
}


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/dev/',
        'STATS_FILE': os.path.join(PROJECT_DIR, 'webpack-stats-dev.json'),
    }
}

FIXTURE_DIRS.append(os.path.join(PROJECT_DIR, "graph_fixtures"),)
