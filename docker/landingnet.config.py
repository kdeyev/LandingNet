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
ELK = elasticsearch.Elasticsearch( ["192.168.203.109"], port=30920)

import json
from jira import JIRA
from jira import JIRAError
products_conf_file = open("/LandingNet/LandingNet/products.conf","r")
PRODUCTS_MAP = json.load(products_conf_file)
JIRA_CLIENT  = JIRA(options={'server': 'http://jira.pdgm.com:8080', 'rest_api_version': 'latest'}, basic_auth=('farmer', 'MkeShrgF6') )

