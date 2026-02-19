import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():
    p = argparse.ArgumentParser(description="Send a basic email via SMTP")
    p.add_argument("--smtp-host", default="localhost")
    p.add_argument("--smtp-port", type=int, default=587)
    p.add_argument("--user", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--to", dest="to_addr", required=True)
    p.add_argument("--subject", default="Hello")
    p.add_argument("--body", default="Hello from Python")
    p.add_argument("--starttls", action="store_true", default=True)
    p.add_argument("--no-starttls", dest="starttls", action="store_false")
    args = p.parse_args()

    msg = MIMEMultipart()
    msg["From"] = args.user
    msg["To"] = args.to_addr
    msg["Subject"] = args.subject
    msg.attach(MIMEText(args.body, "plain", "utf-8"))

    with smtplib.SMTP(args.smtp_host, args.smtp_port, timeout=10) as smtp:
        smtp.ehlo()
        if args.starttls:
            smtp.starttls()
            smtp.ehlo()
        smtp.login(args.user, args.password)
        smtp.sendmail(args.user, [args.to_addr], msg.as_string())
        print("OK: email sent")


if __name__ == "__main__":
    main()
