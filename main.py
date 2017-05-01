#!/usr/bin/python
"""main.py
"""

import time, logging

from common import config, dbm, db



def dbm_main():
    """main
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', filename='./dbm.log', filemode='a')
    
    dbmconfig = config.Config()
    dbmconfig.json_config_load_file()

    dbmonitor = dbm.Dbm(dbmconfig)
    dbmonitor.start()

    db_scan = db.DB('192.168.1.205', 'root', 'sanscout123', 'sanscout', dbmconfig)
    db_scan.start()

    try:
        while True:
            time.sleep(1)
        logging.debug('main function finished')
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'

if __name__ == '__main__':
    dbm_main()
