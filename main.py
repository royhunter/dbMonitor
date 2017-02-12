#!/usr/bin/python

import threading,time
from httpd import httpd


PORT_NUMBER = 8000


def dbmHttpdThread():
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