import settings as creds
import imapclient as imap
from twilio.rest import Client 


# Create SMTP server connection
#smtpObj = smtp.SMTP_SSL('smtp.gmail.com', 465)
#smtpObj.login(creds.USERNAME, creds.PASS)

#smtpObj.sendmail(creds.USERNAME, 'pat@paje.io', 'Subject: Please End Me\nWhut')

# Create IMAP Connection
def update_UIDs():
    imapObj = imap.IMAPClient('imap.gmail.com', ssl=True)
    imapObj.login(creds.USERNAME, creds.PASS)
    imapObj.select_folder('INBOX', readonly=True)

    UIDs = imapObj.gmail_search('@lucidmotors.com')
    UIDs = UIDs[::-1]

    with open('uids.txt', 'r+') as f:
        oldUIDs = f.readline()
        print(oldUIDs)
        print(UIDs)
        if len(oldUIDs) == 0:
            f.write(str(UIDs))
            return

    with open('uids.txt', 'w') as overwrite:
        overwrite.write(str(UIDs))
    send_message(oldUIDs, str(UIDs))


def send_message(str_old, str_new):
    twilioCLI = Client(creds.TWILIO_SID, creds.TWILIO_TOKEN)
    if len(str_old) != len(str_new):
        message = twilioCLI.messages.create(messaging_service_sid='MGadc94b9b70fbb545b1c832b91a2af956', body='New Message from Lucid Motors', to=creds.MY_PHONE)

update_UIDs()
