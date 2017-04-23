import threading
import time
import MySQLdb


class DB(object):

    def __init__(self, db_host, db_user, db_passwd, db_name):
        self.host = db_host
        self.user = db_user
        self.passwd = db_passwd
        self.dbname = db_name
        self.conn = None
        self.curs = None
        self.dbt = threading.Thread(target=self.db_thread,
                                    name='db thread')

    def Start(self):
        print "start db connect"
        self.conn = MySQLdb.connect(host=self.host, port=3306, user=self.user, passwd=self.passwd)
        self.curs = self.conn.cursor()
        self.conn.select_db(self.dbname)
        self.dbt.daemon = True
        self.dbt.start()

    def db_thread(self):

        while 1:
            print "1s"
            select_time = int(time.time()) - 5
            #LPU_QUERY_SQL = "SELECT * FROM LPU_TABLE_0 WHERE MyTimeStamp=" + str(select_time)
            LPU_QUERY_SQL = "SELECT * FROM LPU_TABLE_0 WHERE MyTimeStamp=1492500753"
            print LPU_QUERY_SQL

            self.curs.execute(LPU_QUERY_SQL)
            results = self.curs.fetchall()
            for row in results:
                sequence = row[5]
                loss_signal_event = row[6]
                code_violations = row[7]
                loss_sync_event = row[8]
                lip_event = row[9]
                nos_ols_events = row[10]
                print "sequence = %d, loss_signal_event=%s,code_violations=%s,loss_sync_eventage=%d,lip_event=%s,nos_ols_events=%d" % \
                        (sequence, loss_signal_event, code_violations, loss_sync_event, lip_event, nos_ols_events )



            time.sleep(1)



    