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
        self.lpu_entry_stat = dbm_config.lpu_entry_stat
        self.spu_entry_stat = dbm_config.spu_entry_stat
        self.dbt = threading.Thread(target=self.db_thread,
                                    name='db thread')

    def start(self):
        """start
        """
        print "start db connect"
        self.conn = MySQLdb.connect(host=self.host, port=3306, user=self.user, passwd=self.passwd)
        print "db connect done"
        self.curs = self.conn.cursor()
        self.conn.select_db(self.dbname)
        self.dbt.daemon = True
        self.dbt.start()


    def spu_monitor(self, entrystat, timestamp, itl, name, value):
        if name not in entrystat:
            entry_stat = {"trigger_time": 0,
                          "measure":0,
                          "hit":0,
                          "slot":0,
                          "index":0,
                          "hit_cnt":0,
                          "trigger_cnt":0}
            entrystat[name] = entry_stat

        trigger_time = entrystat[name]["trigger_time"]
        print "last trigger time %d" % trigger_time
        if trigger_time != 0:
            untriggertime = self.dbmconfig.config[key.JSON_GLOBAL_MONITOR][key.JSON_GLB_UNTRIGGER_TIME]
            print "untriggertime is " + str(untriggertime)
            offset = timestamp - trigger_time
            print "%d second passed" % offset
            if timestamp > (trigger_time + untriggertime):
                print "clear stat"
                entrystat[name]["trigger_time"] = 0
                entrystat[name]["slot"] = 0
                entrystat[name]["index"] = 0
            else:
                print "no need send alarm"
                return

        hit = 0
        if entrystat[name]["trigger_time"] == 0:
            print self.dbmconfig.config[key.JSON_SPU_MONITOR]
            if self.dbmconfig.config[key.JSON_SPU_MONITOR][itl][name][key.JSON_OP] == "==":
                print "=="
                if value == self.dbmconfig.config[key.JSON_LPU_MONITOR][itl][name][key.JSON_THRESHOLD]:
                    hit = 1
                else:
                    hit = 0
            elif self.dbmconfig.config[key.JSON_SPU_MONITOR][itl][name][key.JSON_OP] == ">":
                print ">"
                print "value: " + str(value)
                if value > self.dbmconfig.config[key.JSON_SPU_MONITOR][itl][name][key.JSON_THRESHOLD]:
                    hit = 1
                else:
                    hit = 0
            else:
                print "<"
                if value < self.dbmconfig.config[key.JSON_SPU_MONITOR][itl][name][key.JSON_THRESHOLD]:
                    hit = 1
                else:
                    hit = 0

        if hit:
            hitcnt = entrystat[name]["hit_cnt"] + 1
            entrystat[name]["hit_cnt"] = hitcnt

        trigger = self.hit_status(entrystat, hit, name)
        if trigger:
            triggercnt = entrystat[name]["trigger_cnt"] + 1
            entrystat[name]["trigger_cnt"] = triggercnt
            entrystat[name]["trigger_time"] = timestamp
            print "send alarm mail"
            #send_alarm_mail(alarm_str);
    
    
    def entry_monitor(self, entrystat, timestamp, name, value):
        if name not in entrystat:
            entry_stat = {"trigger_time": 0,
                          "measure":0,
                          "hit":0,
                          "slot":0,
                          "index":0,
                          "hit_cnt":0,
                          "trigger_cnt":0}
            entrystat[name] = entry_stat

        trigger_time = entrystat[name]["trigger_time"]
        print "last trigger time %d" % trigger_time
        if trigger_time != 0:
            untriggertime = self.dbmconfig.config[key.JSON_GLOBAL_MONITOR][key.JSON_GLB_UNTRIGGER_TIME]
            print "untriggertime is " + str(untriggertime)
            offset = timestamp - trigger_time
            print "%d second passed" % offset
            if timestamp > (trigger_time + untriggertime):
                print "clear stat"
                entrystat[name]["trigger_time"] = 0
                entrystat[name]["slot"] = 0
                entrystat[name]["index"] = 0
            else:
                print "no need send alarm"
                return

        hit = 0
        if entrystat[name]["trigger_time"] == 0:
            print self.dbmconfig.config[key.JSON_LPU_MONITOR]
            if self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_OP] == "==":
                print "=="
                if value == self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_THRESHOLD]:
                    hit = 1
                else:
                    hit = 0
            elif self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_OP] == ">":
                print ">"
                print "value: " + str(value)
                if value > self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_THRESHOLD]:
                    hit = 1
                else:
                    hit = 0
            else:
                print "<"
                if value < self.dbmconfig.config[key.JSON_LPU_MONITOR][name][key.JSON_THRESHOLD]:
                    hit = 1
                else:
                    hit = 0

        if hit:
            hitcnt = entrystat[name]["hit_cnt"] + 1
            entrystat[name]["hit_cnt"] = hitcnt

        trigger = self.hit_status(entrystat, hit, name)
        if trigger:
            triggercnt = entrystat[name]["trigger_cnt"] + 1
            entrystat[name]["trigger_cnt"] = triggercnt
            entrystat[name]["trigger_time"] = timestamp
            print "send alarm mail"
            #send_alarm_mail(alarm_str);


    def spu_entry_monitor(self, timestamp, itl, name, value):
        """spu_entry_monitor
        """

        if key.JSON_SPU_MONITOR not in self.dbmconfig.config:
            return

        if itl not in self.dbmconfig.config[key.JSON_SPU_MONITOR]:
            return

        if name not in self.dbmconfig.config[key.JSON_SPU_MONITOR][itl]:
            return
        
        if key.JSON_OP not in self.dbmconfig.config[key.JSON_SPU_MONITOR][itl][name]:
            return
        
        if key.JSON_THRESHOLD not in self.dbmconfig.config[key.JSON_SPU_MONITOR][itl][name]:
            return

        if itl not in self.spu_entry_stat:
            self.spu_entry_stat[itl] = {}
        
        self.spu_monitor(self.spu_entry_stat[itl], timestamp, itl, name, value)

    def lpu_entry_monitor(self, timestamp, name, value):
        """lpu_monitor
        """

        if key.JSON_LPU_MONITOR not in self.dbmconfig.config:
            return

        if name not in self.dbmconfig.config[key.JSON_LPU_MONITOR]:
            return

        if key.JSON_OP not in self.dbmconfig.config[key.JSON_LPU_MONITOR][name]:
            return
        
        if key.JSON_THRESHOLD not in self.dbmconfig.config[key.JSON_LPU_MONITOR][name]:
            return

        self.entry_monitor(self.lpu_entry_stat, timestamp, name, value)

        


    def hit_status(self, entrystat, hit, name):
        """hit_status
        """
        print "hit: " + str(hit)
        index = entrystat[name]["index"]
        slot = entrystat[name]["slot"]
        if hit:
            mask = 1 << index
            entrystat[name]["slot"] = slot | mask
        else:
            mask = ~(1 << index)
            entrystat[name]["slot"] = slot & mask

        index = index + 1
        measurements = self.dbmconfig.config[key.JSON_GLOBAL_MONITOR][key.JSON_GLB_MEASURMENTS]
        if index == measurements:
            index = 0

        entrystat[name]["index"] = index
        triggercnt = 0
        slot = entrystat[name]["slot"]
        for i in range(measurements):
            if slot & (1<<i):
                triggercnt = triggercnt + 1

        print "triggercnt is %d" % triggercnt

        if triggercnt >= self.dbmconfig.config[key.JSON_GLOBAL_MONITOR][key.JSON_GLB_TRIGGER_THRE]:
            return 1
        else:
            return 0


    def db_thread(self):
        """db_thread
        """
        #select_time = 1493195084
        while 1:
            time.sleep(1)

            # if key.JSON_SMTP_SERVER not in self.dbmconfig.config:
            #     continue
            
            # if key.JSON_SMTP_PORT not in self.dbmconfig.config:
            #     continue

            # if key.JSON_SMTP_USER not in self.dbmconfig.config:
            #     continue

            # if key.JSON_SMTP_PASSWD not in self.dbmconfig.config:
            #     continue

            # if key.JSON_SMTP_RECV not in self.dbmconfig.config:
            #     continue
            
            # if key.JSON_SMTP_FROM not in self.dbmconfig.config:
            #     continue

            if key.JSON_GLOBAL_MONITOR not in self.dbmconfig.config:
                continue
            
            if key.JSON_GLB_MEASURMENTS not in self.dbmconfig.config[key.JSON_GLOBAL_MONITOR]:
                continue
            
            if key.JSON_GLB_TRIGGER_THRE not in self.dbmconfig.config[key.JSON_GLOBAL_MONITOR]:
                continue
            
            if key.JSON_GLB_UNTRIGGER_TIME not in self.dbmconfig.config[key.JSON_GLOBAL_MONITOR]:
                continue
            

            select_time = int(time.time()) - 5
            #select_time = select_time + 1
            lpu_query_sql = "SELECT * FROM LPU_TABLE_0 WHERE MyTimeStamp=" + str(select_time)
            #lpu_query_sql = "SELECT * FROM LPU_TABLE_0 WHERE MyTimeStamp=1493195084"
            print lpu_query_sql

            self.curs.execute(lpu_query_sql)
            results = self.curs.fetchall()
            if len(results) == 0:
                #print "no entry"
                continue

            for row in results:
                self.lpu_entry_monitor(select_time, "sequence", row[5])
                self.lpu_entry_monitor(select_time, "loss_signal_event", row[6])
                self.lpu_entry_monitor(select_time, "code_violations", row[7])
                self.lpu_entry_monitor(select_time, "loss_sync_event", row[8])
                self.lpu_entry_monitor(select_time, "lip_event", row[9])
                self.lpu_entry_monitor(select_time, "nos_ols_events", row[10])
                self.lpu_entry_monitor(select_time, "link_up_event", row[11])
                self.lpu_entry_monitor(select_time, "frame_err", row[12])
                self.lpu_entry_monitor(select_time, "el_service_frame", row[13])
                self.lpu_entry_monitor(select_time, "fc_service_frame", row[14])
                self.lpu_entry_monitor(select_time, "soff_frame", row[15])
                self.lpu_entry_monitor(select_time, "basic_fc_ls", row[16])
                self.lpu_entry_monitor(select_time, "fc_link_c_frame", row[17])
                self.lpu_entry_monitor(select_time, "cc_state_frame", row[18])
                self.lpu_entry_monitor(select_time, "other_bad_status_frame", row[19])
                self.lpu_entry_monitor(select_time, "task_maga_frame", row[20])
                self.lpu_entry_monitor(select_time, "logins", row[21])
                self.lpu_entry_monitor(select_time, "logouts", row[22])
                self.lpu_entry_monitor(select_time, "abts", row[23])
                self.lpu_entry_monitor(select_time, "notifications", row[24])
                self.lpu_entry_monitor(select_time, "rejects", row[25])
                self.lpu_entry_monitor(select_time, "busy", row[26])
                self.lpu_entry_monitor(select_time, "accepts", row[27])
                self.lpu_entry_monitor(select_time, "loop_init_frames", row[28])
                self.lpu_entry_monitor(select_time, "fps", row[29])
                self.lpu_entry_monitor(select_time, "bps", row[30])
                self.lpu_entry_monitor(select_time, "scsi_fps", row[31])
                self.lpu_entry_monitor(select_time, "scsi_bps", row[32])
                self.lpu_entry_monitor(select_time, "manage_fps", row[33])
                self.lpu_entry_monitor(select_time, "manage_bps", row[34])
                self.lpu_entry_monitor(select_time, "app_data_fps", row[35])
                self.lpu_entry_monitor(select_time, "app_data_bps", row[36])
                self.lpu_entry_monitor(select_time, "total_capacity_percent", row[37])
                self.lpu_entry_monitor(select_time, "total_capacity", row[38])
                self.lpu_entry_monitor(select_time, "scsi_capacity_percent", row[39])
                self.lpu_entry_monitor(select_time, "total_capacity2", row[40])
                self.lpu_entry_monitor(select_time, "manage_capacity_percent", row[41])
                self.lpu_entry_monitor(select_time, "total_capacity3", row[42])
                self.lpu_entry_monitor(select_time, "other_fps", row[43])
                self.lpu_entry_monitor(select_time, "other_bps", row[44])
                self.lpu_entry_monitor(select_time, "other_capacity_percent", row[45])
                self.lpu_entry_monitor(select_time, "total_capacity4", row[46])
                self.lpu_entry_monitor(select_time, "pending_exchange", row[47])
                self.lpu_entry_monitor(select_time, "max_pending_exchange", row[48])
                self.lpu_entry_monitor(select_time, "speed", row[49])
                self.lpu_entry_monitor(select_time, "signal_state", row[50])
                self.lpu_entry_monitor(select_time, "min_frame_to_r_rdy", row[51])
                self.lpu_entry_monitor(select_time, "max_frame_to_r_rdy", row[52])
                self.lpu_entry_monitor(select_time, "avg_frame_to_r_rdy", row[53])
                self.lpu_entry_monitor(select_time, "pending_frame_to_r_rdy", row[54])

            spu_query_sql = "SELECT * FROM SPU_TABLE_0 WHERE MyTimeStamp=" + str(select_time)
            #lpu_query_sql = "SELECT * FROM LPU_TABLE_0 WHERE MyTimeStamp=1493195084"
            print spu_query_sql

            self.curs.execute(spu_query_sql)
            results = self.curs.fetchall()
            if len(results) == 0:
                continue

            for row in results:
                i = row[6]
                t = row[7]
                l = row[8]
                itl = "0x%06x-0x%06x-0x%04x" % (i, t, l)
                print itl
                self.spu_entry_monitor(select_time, itl, "bps", row[10])
                self.spu_entry_monitor(select_time, itl, "fps", row[11])
                self.spu_entry_monitor(select_time, itl, "tmf", row[12])
                self.spu_entry_monitor(select_time, itl, "obsf", row[13])
                self.spu_entry_monitor(select_time, itl, "ccsf", row[14])
                self.spu_entry_monitor(select_time, itl, "rc_issued", row[15])
                self.spu_entry_monitor(select_time, itl, "rc_comp", row[16])
                self.spu_entry_monitor(select_time, itl, "min_rsize", row[17])
                self.spu_entry_monitor(select_time, itl, "max_rsize", row[18])
                self.spu_entry_monitor(select_time, itl, "rd_bps", row[19])
                self.spu_entry_monitor(select_time, itl, "rd_pps", row[20])
                self.spu_entry_monitor(select_time, itl, "min_cmd_to_first", row[21])
                self.spu_entry_monitor(select_time, itl, "max_cmd_to_first", row[22])
                self.spu_entry_monitor(select_time, itl, "avg_cmd_to_first", row[23])
                self.spu_entry_monitor(select_time, itl, "min_last_to_resp", row[24])
                self.spu_entry_monitor(select_time, itl, "max_last_to_resp", row[25])
                self.spu_entry_monitor(select_time, itl, "avg_last_to_resp", row[26])
                self.spu_entry_monitor(select_time, itl, "min_read_exchange_comp", row[27])
                self.spu_entry_monitor(select_time, itl, "max_read_exchange_comp", row[28])
                self.spu_entry_monitor(select_time, itl, "avg_read_exchange_comp", row[29])
                self.spu_entry_monitor(select_time, itl, "write_cmd_issued", row[30])
                self.spu_entry_monitor(select_time, itl, "write_cmd_comp", row[31])
                self.spu_entry_monitor(select_time, itl, "min_wsize", row[32])
                self.spu_entry_monitor(select_time, itl, "max_wsize", row[33])
                self.spu_entry_monitor(select_time, itl, "wd_bps", row[34])
                self.spu_entry_monitor(select_time, itl, "wd_pps", row[35])
                self.spu_entry_monitor(select_time, itl, "min_cmd_to_trans_ready", row[36])
                self.spu_entry_monitor(select_time, itl, "max_cmd_to_trans_ready", row[37])
                self.spu_entry_monitor(select_time, itl, "avg_cmd_to_trans_ready", row[38])
                self.spu_entry_monitor(select_time, itl, "min_trans_ready_to_first", row[39])
                self.spu_entry_monitor(select_time, itl, "max_trans_ready_to_first", row[40])
                self.spu_entry_monitor(select_time, itl, "avg_trans_ready_to_first", row[41])
                self.spu_entry_monitor(select_time, itl, "min_last_data_to_resp", row[42])
                self.spu_entry_monitor(select_time, itl, "max_last_data_to_resp", row[43])
                self.spu_entry_monitor(select_time, itl, "avg_last_data_to_resp", row[44])
                self.spu_entry_monitor(select_time, itl, "min_write_exchange_comp", row[45])
                self.spu_entry_monitor(select_time, itl, "max_write_exchange_comp", row[46])
                self.spu_entry_monitor(select_time, itl, "avg_write_exchange_comp", row[47])
                self.spu_entry_monitor(select_time, itl, "pending_exchanges", row[48])
                self.spu_entry_monitor(select_time, itl, "min_pending_exchanges", row[49])
                self.spu_entry_monitor(select_time, itl, "max_pending_exchanges", row[50])
                self.spu_entry_monitor(select_time, itl, "bps_percent", row[51])
                self.spu_entry_monitor(select_time, itl, "fps_percent", row[52])