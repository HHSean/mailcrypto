##############
# WORKING CODE
##############

import smtplib, ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv("../.env")

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")


def send_email(recipient, key="", subject="accept your crypto", amount=0, message=''):
    # Create a text/plain message

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, context=context) as server:
        server.login(MAIL_USERNAME, MAIL_PASSWORD)

        body = f"""
Hi, someone is trying to send you crypto!

    Amount: {amount}
    Message: {message}
    Key: {key}
        
If you want to claim it, you can do so directly at https://mailcrypto.xyz/claim/{key}
(DO **NOT** SEND THIS LINK TO ANYONE ELSE!)


We're happy to provide this service free of charge!

If you want to no longer receive emails from us, you can do so at https://mailcrypto.xyz/unsubscribe/{key}
"""

        msg = EmailMessage()
        
        msg["Subject"] = subject
        msg.set_content(body)
        msg["From"] = "gm@mailcrypto.xyz"
        msg["To"] = recipient
        server.send_message(msg)
        return


def send_admin_email(**kwargs):
    # sends admin email to mailcrypto@hugomontenegro.com
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, context=context) as server:
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        content = f"New event in mailcrypto.xyz. \nArguments:"
        for k, v in kwargs.items():
            content += f"\n{k}: {v}"
        msg = EmailMessage()
        msg["Subject"] = "New event in mailcrypto.xyz"
        msg.set_content(content)
        msg["From"] = "admin@mailcrypto.xyz"
        msg["To"] = "mailcrypto@hugomontenegro.com"
        server.send_message(msg)
        return

if __name__ == "__main__":
    # send test email to test@hugomontenegro.com
    send_email("test@hugomontenegro.com", amount=1, message="test")