"""db.py
"""

import threading
import time

import MySQLdb

from . import key


class DB(object):
    """CLASS DB
    """
    def __init__(self, db_host, db_user, db_passwd, db_name, dbm_config):
        self.host = db_host
        self.user = db_user
        self.passwd = db_passwd
        self.dbname = db_name
        self.dbmconfig = dbm_config
        self.conn = None
        self.curs = None
        self.lpu_entry_stat = {}
        self.dbt = threading.Thread(target=self.db_thread,
                                    name='db thread')

    def start(self):
        """start
        """
        print "start db connect"
        self.conn = MySQLdb.connect(host=self.host, port=3306, user=self.user, passwd=self.passwd)
        self.curs = self.conn.cursor()
        self.conn.select_db(self.dbname)
        self.dbt.daemon = True
        self.dbt.start()

    def lpu_entry_monitor(self, timestamp, name, value):
        """lpu_monitor
        """
        print "lpu_entry_monitor"
        print timestamp
        print name
        print value

        if self.dbmconfig.config[key.JSON_LPU_MONITOR] is None:
            return

        if self.dbmconfig.config[key.JSON_LPU_MONITOR][name] is None:
            return

        if self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_OP] is None:
            return

        if self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_THRESHOLD] is None:
            return

        if self.lpu_entry_stat[name] is None:
            entry_stat = {"trigger_time": 0,
                          "measure":0,
                          "hit":0,
                          "slot":0,
                          "index":0,
                          "hit_cnt":0,
                          "trigger_cnt":0}
            self.lpu_entry_stat[name] = entry_stat

        trigger_time = self.lpu_entry_stat[name]["trigger_time"]
        if trigger_time != 0:
            untriggertime = self.dbmconfig[key.JSON_GLOBAL_MONITOR][key.JSON_GLB_UNTRIGGER_TIME]
            if timestamp > (trigger_time + untriggertime):
                self.lpu_entry_stat[name]["trigger_time"] = 0
                self.lpu_entry_stat[name]["slot"] = 0
                self.lpu_entry_stat[name]["index"] = 0

        if self.lpu_entry_stat[name]["trigger_time"] == 0:
            if self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_OP] == "==":
                if value == self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_THRESHOLD]:
                    hit = 1
                else:
                    hit = 0
            elif self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_OP] == ">":
                if value > self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_THRESHOLD]:
                    hit = 1
                else:
                    hit = 0
            else:
                if value < self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_THRESHOLD]:
                    hit = 1
                else:
                    hit = 0

        if hit:
            hitcnt = self.lpu_entry_stat[name]["hit_cnt"] + 1
            self.lpu_entry_stat[name]["hit_cnt"] = hitcnt

        trigger = hit_status(hit)
        if trigger:
            triggercnt = self.lpu_entry_stat[name]["trigger_cnt"] + 1
            self.lpu_entry_stat[name]["trigger_cnt"] = triggercnt
            triggertime = self.lpu_entry_stat[name]["trigger_time"] + 1
            self.lpu_entry_stat[name]["trigger_time"] = triggertime
            #send_alarm_mail(alarm_str);


        def hit_status(hit):
            """hit_status
            """
            print hit
            index = self.lpu_entry_stat[name]["index"]
            slot = self.lpu_entry_stat[name]["slot"]
            if hit:
                mask = 1 << index
                self.lpu_entry_stat[name]["slot"] = slot | mask
            else:
                mask = ~(1 << index)
                self.lpu_entry_stat[name]["slot"] = slot & mask

            index = index + 1
            measurements = self.dbmconfig[key.JSON_GLOBAL_MONITOR][key.JSON_GLB_MEASURMENTS]
            if index == measurements:
                index = 0

            self.lpu_entry_stat[name]["index"] = 0
            triggercnt = 0
            slot = self.lpu_entry_stat[name]["slot"]
            for i in range(measurements):
                if slot & (1<<i):
                    triggercnt = triggercnt + 1

            if triggercnt >= self.dbmconfig[key.JSON_GLOBAL_MONITOR][key.JSON_GLB_TRIGGER_THRE]:
                return 1
            else:
                return 0



    def db_thread(self):
        """db_thread
        """
        while 1:
            print "1s"
            select_time = int(time.time()) - 5
            lpu_query_sql = "SELECT * FROM LPU_TABLE_0 WHERE MyTimeStamp=" + str(select_time)
            #LPU_QUERY_SQL = "SELECT * FROM LPU_TABLE_0 WHERE MyTimeStamp=1492500753"
            print lpu_query_sql

            self.curs.execute(lpu_query_sql)
            results = self.curs.fetchall()
            if results is None:
                continue

            for row in results:
                self.lpu_entry_monitor(select_time, "sequence", row[5])
                loss_signal_event = row[6]
                code_violations = row[7]
                loss_sync_event = row[8]
                lip_event = row[9]
                nos_ols_events = row[10]
                link_up_event = row[11]
                frame_err = row[12]
                el_service_frame = row[13]
                fc_service_frame = row[14]
                soff_frame = row[15]
                basic_fc_ls = row[16]
                fc_link_c_frame = row[17]
                cc_state_frame = row[18]
                other_bad_status_frame = row[19]
                task_maga_frame = row[20]
                logins = row[21]
                logouts = row[22]
                abts = row[23]
                notifications = row[24]
                rejects = row[25]
                busy = row[26]
                accepts = row[27]
                loop_init_frames = row[28]
                fps = row[29]
                bps = row[30]
                scsi_fps = row[31]
                scsi_bps = row[32]
                manage_fps = row[33]
                manage_bps = row[34]
                app_data_fps = row[35]
                app_data_bps = row[36]
                total_capacity_percent = row[37]
                total_capacity = row[38]
                scsi_capacity_percent = row[39]
                total_capacity2 = row[40]
                manage_capacity_percent = row[41]
                total_capacity3 = row[42]
                other_fps = row[43]
                other_bps = row[44]
                other_capacity_percent = row[45]
                total_capacity4 = row[46]
                pending_exchange = row[47]
                max_pending_exchange = row[48]
                speed = row[49]
                signal_state = row[50]
                min_frame_to_r_rdy = row[51]
                max_frame_to_r_rdy = row[52]
                avg_frame_to_r_rdy = row[53]
                pending_frame_to_r_rdy = row[54]
                print "sequence = %d, loss_signal_event=%d,code_violations=%d,loss_sync_eventage=%d,lip_event=%d,nos_ols_events=%d" % \
                        (sequence, loss_signal_event, code_violations, loss_sync_event, lip_event, nos_ols_events )



            time.sleep(1)
