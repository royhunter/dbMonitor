#!/usr/bin/python
import json
import key

######################
# URL GET
######################
def root_get(myHttpHandler):
    myHttpHandler.reply_ok('Hello, Welcome dbMonitor')

def version_get(myHttpHandler):
    myHttpHandler.reply_ok(myHttpHandler.path)

def config_get(myHttpHandler):
    myHttpHandler.reply_ok(myHttpHandler.path)

######################
# URL POST
######################
def config_post(myHttpHandler):
    print "config_post"
    content_len = int(myHttpHandler.headers.getheader('content-length', 0))
    content = myHttpHandler.rfile.read(content_len)
    print content
    config_json_parser(content)
    myHttpHandler.reply_ok(content)

def config_json_parser(json_string):
    print "config_json_parser"
    print key.JSON_SMTP_SERVER
    x = json.loads(json_string)
    print x
    print x['name']