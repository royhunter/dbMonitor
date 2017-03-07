#!/usr/bin/python
"""main.py
"""

import time

from common import config, dbm



def dbm_main():
    """main
    """
    dbmconfig = config.Config()
    dbmconfig.json_config_load_file()

    dbmonitor = dbm.Dbm(dbmconfig)
    dbmonitor.start()
    try:
        while True:
            time.sleep(1)
        print 'main function finished'
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'

if __name__ == '__main__':
    dbm_main()
