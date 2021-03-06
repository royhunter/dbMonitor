#!/usr/bin/python
"""config.py
"""
import logging

import json
import os
from . import key

class Config(object):
    """Config Class
    """
    CONFIG_FILE_NAME = './config.json'

    def __init__(self):
        self.lpu_entry_stat = {}
        self.spu_entry_stat = {}
        self.config = {}
        self.spu_monitor = {}  # itl_name is key

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
        logging.debug(self.config)

    def config_json_parser(self, json_string):
        """config_json_parser
        """
        json_obj = json.loads(json_string)
        self.config = json_obj
        logging.debug(self.config)
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

    def json_lpu_monitor_parser(self, json_object):
        """json_lpu_monitor_parser
        """
        if key.JSON_LPU_MONITOR not in json_object:
            return

        self.config[key.JSON_LPU_MONITOR] = json_object[key.JSON_LPU_MONITOR]


    def json_spu_monitor_parser(self, json_object):
        """json_spu_monitor_parser
        """
        if key.JSON_SPU_MONITOR not in json_object:
            return

        itl_list = json_object[key.JSON_SPU_MONITOR]
        #print itl_list
        if itl_list is None:
            return

        for itl in itl_list:
            itl_name = itl[key.JSON_ITL]
            itl_op = itl[key.JSON_ITL_OPERATION]
            if itl_op == key.JSON_ITL_UPDATE:
                self.spu_monitor[itl_name] = itl
                del self.spu_monitor[itl_name][key.JSON_ITL_OPERATION]
            elif self.spu_monitor.has_key(itl_name) and itl_op == key.JSON_ITL_DELETE:
                del self.spu_monitor[itl_name]

        del self.config[key.JSON_SPU_MONITOR]
        self.config[key.JSON_SPU_MONITOR] = []
        for itl in self.spu_monitor:
            self.config[key.JSON_SPU_MONITOR].append(self.spu_monitor[itl])


