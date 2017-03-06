from email.mime.text import MIMEText
import smtplib

msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')


from_addr = 'roy.luo@sanscout.com'
password = '!Thankyou1'
smtp_server = 'smtp.emailsrvr.com'
to_addr = '181006606@qq.com'


server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

