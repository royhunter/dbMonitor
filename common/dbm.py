"""dbm.py
"""

import threading

from common import httpd, url


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
        self.urlhandle.url_get_mapping_register('/debug', url.debug_get)
        self.urlhandle.url_post_mapping_register('/config', url.config_post)
        self.urlhandle.url_post_mapping_register('/testmail', url.test_mail)
        httpserver = httpd.HttpServer(httpd.HttpServer.PORT_NUMBER,
                                      self.config,
                                      self.urlhandle)
        httpserver.runserver()

    def start(self):
        """start
        """
        self.httpd.daemon = True
        self.httpd.start()
