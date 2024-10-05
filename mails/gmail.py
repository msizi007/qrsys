import smtplib
from json import load

with open('mails/config.json') as json_file:
    data = load(json_file)

SENDER_EMAIL = data.get('email_address')
PASSWORD = data.get('password')

def send(receiver_email, subject, body):

    sever = smtplib.SMTP('smtp.gmail.com', 587)
    sever.starttls()
    sever.login(SENDER_EMAIL, PASSWORD)
    message = f'Subject: {subject}\n\n{body}'

    sever.sendmail(SENDER_EMAIL, receiver_email, message)
    sever.quit()


