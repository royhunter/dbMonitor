#!/usr/bin/python
import json
from . import key

config = {}



def JSON_SMTP_Parser(json_object):
    if key.JSON_SMTP_SERVER in json_object:
        config[key.JSON_SMTP_SERVER] = json_object[key.JSON_SMTP_SERVER]
    if key.JSON_SMTP_PASSWD in json_object:
        config[key.JSON_SMTP_PASSWD] = json_object[key.JSON_SMTP_PASSWD]
    if key.JSON_SMTP_USER in json_object:
        config[key.JSON_SMTP_USER] = json_object[key.JSON_SMTP_USER]
    if key.JSON_SMTP_PORT in json_object:
        config[key.JSON_SMTP_PORT] = json_object[key.JSON_SMTP_PORT]
    if key.JSON_SMTP_RECV in json_object:
        config[key.JSON_SMTP_RECV] = json_object[key.JSON_SMTP_RECV]
    if key.JSON_SMTP_FROM in json_object:
        config[key.JSON_SMTP_FROM] = json_object[key.JSON_SMTP_FROM]

def JSON_GLOBAL_Monitor_Parser(json_object):
    glb_monitor = {}

    if key.JSON_GLOBAL_MONITOR not in json_object:
        return

    glb_monitor_para = json_object[key.JSON_GLOBAL_MONITOR]
    
    if key.JSON_GLB_MEASURMENTS in glb_monitor_para:
        glb_monitor[key.JSON_GLB_MEASURMENTS] = glb_monitor_para[key.JSON_GLB_MEASURMENTS]

    if key.JSON_GLB_TRIGGER_THRE in glb_monitor_para:
        glb_monitor[key.JSON_GLB_TRIGGER_THRE] = glb_monitor_para[key.JSON_GLB_TRIGGER_THRE]

    if key.JSON_GLB_UNTRIGGER_TIME in glb_monitor_para:
        glb_monitor[key.JSON_GLB_UNTRIGGER_TIME] = glb_monitor_para[key.JSON_GLB_UNTRIGGER_TIME]

    if glb_monitor:
        config[key.JSON_GLOBAL_MONITOR] = glb_monitor
    else:
        return

def json_config_save_file():
    fp = open('./config.json', 'w')
    json.dump(config, fp)
    fp.close()

def json_config_load_file():
    fp = open('./config.json', 'r')
    config = json.load(fp)
    fp.close()
    print config


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
    json_obj = json.loads(json_string)
    
    # SMTP Config
    JSON_SMTP_Parser(json_obj)

    # Global Monitor Para
    JSON_GLOBAL_Monitor_Parser(json_obj)

    print config
    json_config_save_file()
        
