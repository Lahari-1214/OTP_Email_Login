import smtplib
from email.message import EmailMessage

def send_otp(receiver, otp):

    sender = "your_email@gmail.com"
    password = "app_password"

    msg = EmailMessage()
    msg['Subject'] = "Your OTP Code"
    msg['From'] = sender
    msg['To'] = receiver

    msg.set_content(f"Your OTP is {otp}")

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(sender,password)
        smtp.send_message(msg)