import smtplib
from email.message import EmailMessage

def send_otp(receiver, otp):

    sender = "leelanarayan1214@gmail.com"
    password = "app password here" #generate app password from google account and use here

    msg = EmailMessage()
    msg['Subject'] = "Your OTP Code for Login 🔐"
    msg['From'] = sender
    msg['To'] = receiver

    msg.set_content(f"Your OTP is {otp}")

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(sender,password)
        smtp.send_message(msg)