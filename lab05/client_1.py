import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import MY_PASSWORD

MY_EMAIL = "yanin.alex2003@yandex.ru"

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--email", help="Адрес получателя")
    p.add_argument("--subject",  help="Тема")
    p.add_argument("--content",  help="Контент")
    p.add_argument("--format", help="txt ли html")
    args = p.parse_args()

    msg = MIMEMultipart()
    msg["From"] = MY_EMAIL
    msg["To"]   = args.email
    msg["Subject"] = args.subject

    if args.format == "html":
        msg.attach(MIMEText(args.content, 'html'))
    else:
        msg.attach(MIMEText(args.content, 'plain'))

    with smtplib.SMTP("smtp.yandex.ru", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.send_message(msg)
