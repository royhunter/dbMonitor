#!/usr/bin/python
"""main.py
"""

import threading
import time

from common import httpd, url, config



class Dbm(object):
    """Dbm Class
    """

    def __init__(self, dbmconfig):
        self.config = dbmconfig
        self.urlhandle = httpd.ProxyUrlHandle()
        self.httpd = threading.Thread(target=self.httpd_thread,
                                      name='dbm thread')

    def httpd_thread(self):
        """httpd_thread
        """
        self.urlhandle.url_get_mapping_register('/', url.root_get)
        self.urlhandle.url_get_mapping_register('/version', url.version_get)
        self.urlhandle.url_get_mapping_register('/config', url.config_get)
        self.urlhandle.url_post_mapping_register('/config', url.config_post)
        httpserver = httpd.HttpServer(httpd.HttpServer.PORT_NUMBER,
                                      self.config,
                                      self.urlhandle)
        httpserver.runserver()

    def start(self):
        """start
        """
        self.httpd.daemon = True
        self.httpd.start()


def dbm_main():
    """main
    """
    dbmconfig = config.Config()
    dbmconfig.json_config_load_file()

    dbm = Dbm(dbmconfig)
    dbm.start()
    try:
        while True:
            time.sleep(1)
        print 'main function finished'
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'

if __name__ == '__main__':
    dbm_main()
