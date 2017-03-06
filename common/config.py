#!/usr/bin/python
"""config.py
"""

import json
import os
from . import key

class Config(object):
    """Config Class
    """
    CONFIG_FILE_NAME = './config.json'

    def __init__(self):
        self.config = {}

    def json_config_save2file(self):
        """json_config_save_file
        """
        file_p = open(Config.CONFIG_FILE_NAME, 'w')
        json.dump(self.config, file_p)
        file_p.close()

    def json_config_load_file(self):
        """json_config_load_file
        """
        if os.path.exists(Config.CONFIG_FILE_NAME) is False:
            return
        file_p = open(Config.CONFIG_FILE_NAME, 'r')
        self.config = json.load(file_p)
        file_p.close()
        print self.config

    def config_json_parser(self, json_string):
        """config_json_parser
        """
        print "config_json_parser"
        print key.JSON_SMTP_SERVER
        json_obj = json.loads(json_string)

        # SMTP Config
        self.json_smtp_parser(json_obj)

        # Global Monitor Para
        self.json_global_monitor_parser(json_obj)

        print self.config
        self.json_config_save2file()

    def json_smtp_parser(self, json_object):
        """json_smtp_parser
        """
        if key.JSON_SMTP_SERVER in json_object:
            self.config[key.JSON_SMTP_SERVER] = json_object[key.JSON_SMTP_SERVER]
        if key.JSON_SMTP_PASSWD in json_object:
            self.config[key.JSON_SMTP_PASSWD] = json_object[key.JSON_SMTP_PASSWD]
        if key.JSON_SMTP_USER in json_object:
            self.config[key.JSON_SMTP_USER] = json_object[key.JSON_SMTP_USER]
        if key.JSON_SMTP_PORT in json_object:
            self.config[key.JSON_SMTP_PORT] = json_object[key.JSON_SMTP_PORT]
        if key.JSON_SMTP_RECV in json_object:
            self.config[key.JSON_SMTP_RECV] = json_object[key.JSON_SMTP_RECV]
        if key.JSON_SMTP_FROM in json_object:
            self.config[key.JSON_SMTP_FROM] = json_object[key.JSON_SMTP_FROM]

    def json_global_monitor_parser(self, json_object):
        """json_global_monitor_parser
        """
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
            self.config[key.JSON_GLOBAL_MONITOR] = glb_monitor
