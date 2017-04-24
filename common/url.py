
"""url.py
"""
import json

from . import config, key


######################
# URL GET
######################
def root_get(dbmconfig, http_handle):
    """root_get
    """
    dbmconfig.json_config_load_file()
    http_handle.reply_ok('Hello, Welcome dbMonitor')


def version_get(dbmconfig, http_handle):
    """version_get
    """
    http_handle.reply_ok(http_handle.path)

def config_get(dbmconfig, http_handle):
    """config_get
    """
    json_str = json.dumps(dbmconfig.config)
    http_handle.reply_ok(json_str)

def debug_get(dbmconfig, http_handle):
    """debug_get
    """
    json_str = json.dumps(dbmconfig.config)
    http_handle.reply_ok(json_str)


######################
# URL POST
######################
def config_post(dbmconfig, http_handle):
    """config_post
    """
    print "config_post"
    content_len = int(http_handle.headers.getheader('content-length', 0))
    content = http_handle.rfile.read(content_len)
    print content
    dbmconfig.config_json_parser(content)
    http_handle.reply_ok(content)


