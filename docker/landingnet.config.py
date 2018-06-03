import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SQLALCHEMY_DATABASE_URI = "postgresql://landingnet:password@postgresql:5432/landingnetdb" 
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "tools", "db_repository")
MINIDUMP_UPDLOAD_DIR = "minidumps"
BREAKPAD_DEBUG_SYMBOLS_DIR = "breakpad-debug-symbols"
DEBUG_SYMBOLS_DIR = "debug-symbols"
STACKWALKER = "/breakpad/bin/stackwalker"
TITLE = "LandingNet"
ELK_INDEX = "crashes"
ELK_DOCTYPE = "crash"

import elasticsearch
ELK = elasticsearch.Elasticsearch( ["elk"], port=9200)
