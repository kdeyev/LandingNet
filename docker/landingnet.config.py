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

ELK = None
import elasticsearch
ELK = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
ELK_index = 'crashes'
ELK_docType = 'crash'