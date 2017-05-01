
"""url.py
"""
import json,logging
from email.mime.text import MIMEText
import smtplib
from . import config, key


######################
# URL GET
######################
def root_get(dbmconfig, http_handle):
    """root_get
    """
    dbmconfig.json_config_load_file()
    http_handle.reply_ok('Hello, Welcome dbMonitor')


def version_get(dbmconfig, http_handle):
    """version_get
    """
    http_handle.reply_ok("dbMonitor version v1.0.0")

def config_get(dbmconfig, http_handle):
    """config_get
    """
    json_str = json.dumps(dbmconfig.config)
    http_handle.reply_ok(json_str)

def debug_get(dbmconfig, http_handle):
    """debug_get
    """
    json_str = json.dumps(dbmconfig.lpu_entry_stat)
    http_handle.reply_ok(json_str)


######################
# URL POST
######################
def config_post(dbmconfig, http_handle):
    """config_post
    """
    logging.debug("config_post")
    content_len = int(http_handle.headers.getheader('content-length', 0))
    content = http_handle.rfile.read(content_len)
    logging.debug(content)
    dbmconfig.config_json_parser(content)
    http_handle.reply_ok(content)

def test_mail(dbmconfig, http_handle):

    if key.JSON_SMTP_SERVER not in dbmconfig.config:
        logging.debug("smtp server is null")
        http_handle.reply_ok("smtp server is null")
        return
    
    if key.JSON_SMTP_PORT not in dbmconfig.config:
        logging.debug("smtp port is null")
        http_handle.reply_ok("smtp port is null")
        return

    if key.JSON_SMTP_USER not in dbmconfig.config:
        logging.debug("smtp user is null")
        http_handle.reply_ok("smtp user is null")
        return

    if key.JSON_SMTP_PASSWD not in dbmconfig.config:
        logging.debug("smtp passwd is null")
        http_handle.reply_ok("smtp passwd is null")
        return

    if key.JSON_SMTP_RECV not in dbmconfig.config:
        logging.debug("smtp recv is null")
        http_handle.reply_ok("smtp recv is null")
        return
    
    if key.JSON_SMTP_FROM not in dbmconfig.config:
        logging.debug("smtp from is null")
        http_handle.reply_ok("smtp from is null")
        return

    msg = MIMEText("test mail form sanscout", 'plain', 'utf-8')
    
    smtp_server = dbmconfig.config[key.JSON_SMTP_SERVER]
    from_addr = dbmconfig.config[key.JSON_SMTP_FROM]
    to_addr = dbmconfig.config[key.JSON_SMTP_RECV]
    user = dbmconfig.config[key.JSON_SMTP_USER]
    password = dbmconfig.config[key.JSON_SMTP_PASSWD]
    port = dbmconfig.config[key.JSON_SMTP_PORT]

    server = smtplib.SMTP(smtp_server, port)
    server.set_debuglevel(1)
    try:
        server.login(user, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    except:
        logging.debug("test mail error")
        http_handle.reply_ok("test mail error")
    else:
        http_handle.reply_ok("test mail done")


