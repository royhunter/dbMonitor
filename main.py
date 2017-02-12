#!/usr/bin/python

import threading,time
from httpd import httpd
from config import config

PORT_NUMBER = 8000


def dbmHttpdThread():
    httpd.url_get_mapping_register('/', config.root_get)
    httpd.url_get_mapping_register('/version', config.version_get)
    httpd.url_get_mapping_register('/config', config.config_get)
    httpd.url_post_mapping_register('/config', config.config_post)
    dbmHttpd = httpd.dbmHttpServer(PORT_NUMBER)
    dbmHttpd.Run()



def main():
    t = threading.Thread(target = dbmHttpdThread, name = 'dbm thread')
    t.daemon = True
    t.start()
    try:
        while True:
            time.sleep(1)
        print 'main function finished'
    except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            


if __name__ == '__main__':
    main()