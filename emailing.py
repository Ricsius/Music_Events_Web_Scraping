import os
import smtplib
from email.message import EmailMessage

HOST = "smtp.gmail.com"
PORT = 465
EMAIL = os.getenv("MY_MAIL")
PASSWORD = os.getenv("PEMAIL_PASSWORD")

def send_email(message):
    email_message = EmailMessage()
    email_message["Subject"] = "New music event"
    email_message.set_content(message)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL, PASSWORD)
    gmail.sendmail(EMAIL, EMAIL, email_message.as_string())
    gmail.quit()