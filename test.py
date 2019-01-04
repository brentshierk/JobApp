from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

msg = MIMEMultipart()
msg['From'] = 'uncorrupted667@gmail.com'
msg['to'] = 'brent@koi.gg'
password = 'roxxy123'
msg['subject'] = 'test123test'

body = 'testing sending an email with python!!'
msg.attach(MIMEText(body,'html'))
print(msg)

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(msg['From'], password)
server.sendmail(msg['From'],msg['To'],msg.as_string())
server.quit()