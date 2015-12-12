#!/usr/bin/python
# -*- coding: utf-8 -*- 

# for Google docs
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

# for mailing stuff
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# for xmpp support
import xmpp

# other
import datetime

# docs-8cb74cbd9fgs.json used for OAuth with google docs
json_key = json.load(open('docs-8cb74cbd9fgs.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)

# Scheduler_xls should be already created, see format explanation below
sh = gc.open("Scheduler_xls")
worksheet = sh.get_worksheet(0)

# If you use non-ascii (cyrillic) characters for email/jabber notifications - use forced unicode encoding due to prevent issues
what_txt    = u'What should be done: '
when_txt    = u'Event timestamp: '
tz_txt      = u' GMT'
details_txt = u'Comments: '
alert_txt   = "--------------------------------------\n" + u'Notification created: '

# Email notification function
def email_notification(subject, creation_date, execution_date, description):
  mail_from = 'user.from@domain.com'
  mail_to   = 'user.to@example.com'
  mail_pass = 'strong_password'

  msg = MIMEMultipart()
  msg['From'] = mail_from
  msg['To'] = mail_to
  msg['Subject'] = "[Scheduler] " + subject
  message = what_txt + subject + "\n" + when_txt + execution_date + tz_txt + "\n" + details_txt + description +  "\n\n" + alert_txt + creation_date + tz_txt
  msg.attach(MIMEText(message.encode('utf-8'), 'plain', 'utf-8'))

  mailserver = smtplib.SMTP_SSL('mail.domain.com', 465)
  mailserver.ehlo()
  mailserver.login(mail_from, mail_pass)
  mailserver.sendmail(mail_from,mail_to,msg.as_string())
  mailserver.quit()

# Jabber notification function
def jabber_notification(message):
   user="someuser@gmail.com"
   password="strongest_password"
   to='someotheruser@gmail.com'

   jid = xmpp.protocol.JID(user)
   C = xmpp.Client(jid.getDomain(),debug=[])
   if not C.connect((jid.getDomain(),5223)):
       raise IOError('Can not connect')
   if not C.auth(jid.getNode(),password):
       raise IOError('Can not auth with server')

   # use following to get list of contacts
   C.sendInitPresence(requestRoster=1)
   C.send(xmpp.Message(to, message))

# Looping through all needed records in xls worksheet
index = 2
values_list = worksheet.col_values(2)
print u'[Scheduler] We found these events with 10 min deadline:'
for value in values_list[1:]:
   now_date                 = datetime.datetime.now()   
   execution_date           = worksheet.acell('B'+str(index)).value
   execution_date_formatted = datetime.datetime.strptime(execution_date, "%d.%m.%Y %H:%M:%S")

   if execution_date_formatted > now_date:
       delta = execution_date_formatted - now_date
       # divmod return results in X minutes, Y seconds; delta acceptable options: delta.days, delta.seconds, delta.microseconds
       # print divmod(delta.days * 86400 + delta.seconds, 60)
       if delta.days == 0 and delta.seconds <= 600:
           creation_date  = worksheet.acell('A'+str(index)).value
           subject        = worksheet.acell('C'+str(index)).value
           description    = worksheet.acell('D'+str(index)).value

           print str(index) + ") delta (<10min) = " + str(delta) + "\n" + what_txt + subject + "\n" + when_txt + execution_date + tz_txt + "\n" + details_txt + description + "\n" + alert_txt + creation_date + tz_txt
           print "Now its time to send alerts..."
	   email_notification(subject, creation_date, execution_date, description)
           jabber_msg = "[Scheduler]" + "\n" + what_txt + subject + "\n" + when_txt + execution_date + tz_txt + "\n" + details_txt + description + "\n" + alert_txt + creation_date + tz_txt
           jabber_notification(jabber_msg.encode('utf-8'))
           print "--------------------------------------"

   index +=1

