from email.mime.text import MIMEText
import smtplib

msg = MIMEText('hello, send by Dbm...', 'plain', 'utf-8')


from_addr = 'roy.luo@sanscout.com'
user = 'roy.luo@sanscout.com'
password = '!Thankyou'
smtp_server = 'smtp.emailsrvr.com'
to_addr = '181006606@qq.com'


server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(user, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

