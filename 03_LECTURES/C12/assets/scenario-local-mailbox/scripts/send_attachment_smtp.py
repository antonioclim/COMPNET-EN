import argparse
import mimetypes
import smtplib
from pathlib import Path
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders


def main():
    p = argparse.ArgumentParser(description="Send an email with one attachment via SMTP")
    p.add_argument("--smtp-host", default="localhost")
    p.add_argument("--smtp-port", type=int, default=587)
    p.add_argument("--user", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--to", dest="to_addr", required=True)
    p.add_argument("--subject", default="Attachment from Python")
    p.add_argument("--body", default="This email contains an attachment.")
    p.add_argument("--file", required=True, help="Path to attachment")
    p.add_argument("--starttls", action="store_true", default=True)
    p.add_argument("--no-starttls", dest="starttls", action="store_false")
    args = p.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"Attachment not found: {path}")

    ctype, _ = mimetypes.guess_type(str(path))
    if not ctype:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    msg = MIMEMultipart()
    msg["From"] = args.user
    msg["To"] = args.to_addr
    msg["Subject"] = args.subject
    msg.attach(MIMEText(args.body, "plain", "utf-8"))

    with path.open("rb") as f:
        part = MIMEBase(maintype, subtype)
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{path.name}"')
    msg.attach(part)

    with smtplib.SMTP(args.smtp_host, args.smtp_port, timeout=10) as smtp:
        smtp.ehlo()
        if args.starttls:
            smtp.starttls()
            smtp.ehlo()
        smtp.login(args.user, args.password)
        smtp.sendmail(args.user, [args.to_addr], msg.as_string())
        print("OK: email sent with attachment")


if __name__ == "__main__":
    main()
