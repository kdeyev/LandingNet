import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SQLALCHEMY_DATABASE_URI = "postgresql://landingnet:password@postgresql:5432/landingnetdb" 
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "tools", "db_repository")
MINIDUMP_UPDLOAD_DIR = "minidumps"
BREAKPAD_DEBUG_SYMBOLS_DIR = "breakpad-debug-symbols"
DEBUG_SYMBOLS_DIR = "debug-symbols"
STACKWALKER = "/breakpad/bin/stackwalker"
TITLE = "Paradigm Crash Collector"
ELK_INDEX = "crashes"
ELK_DOCTYPE = "crash"


ELK = None
PRODUCTS_MAP = None
JIRA_CLIENT  = None
PRODUCTS_MAP = None

if os.environ.has_key("ELK_SERVER"):    
    try:
        import elasticsearch
        ELK = elasticsearch.Elasticsearch( os.environ["ELK_SERVER"], port=9200)
    except:
        ELK = None

if os.environ.has_key("JIRA_SERVER") and os.environ.has_key("JIRA_USER") and os.environ.has_key("JIRA_PASSWD"):
    try:
        import json
        from jira import JIRA
        from jira import JIRAError
        products_conf_file = open("/LandingNet/LandingNet/products.conf","r")
        PRODUCTS_MAP = json.load(products_conf_file)
        JIRA_CLIENT  = JIRA(options={'server': os.environ["ELK_SERVER"], 'rest_api_version': 'latest'}, basic_auth=(os.environ["JIRA_USER"], os.environ["JIRA_PASSWD"]) )
    except:
        PRODUCTS_MAP = None
        JIRA_CLIENT  = None
        PRODUCTS_MAP = None
