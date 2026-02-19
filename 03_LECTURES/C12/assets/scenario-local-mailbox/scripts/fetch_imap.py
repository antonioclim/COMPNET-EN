import argparse
import imaplib
from email.parser import BytesParser
from email.policy import default


def main():
    p = argparse.ArgumentParser(description="Fetch latest UNSEEN email via IMAP and print basic fields")
    p.add_argument("--imap-host", default="localhost")
    p.add_argument("--imap-port", type=int, default=143)
    p.add_argument("--user", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--mailbox", default="INBOX")
    args = p.parse_args()

    # Use SSL if common SSL port:
    if args.imap_port == 993:
        imap = imaplib.IMAP4_SSL(args.imap_host, args.imap_port)
    else:
        imap = imaplib.IMAP4(args.imap_host, args.imap_port)

    try:
        imap.login(args.user, args.password)
        imap.select(args.mailbox)
        status, data = imap.search(None, "UNSEEN")
        if status != "OK":
            print("IMAP search failed:", status, data)
            return

        ids = data[0].split()
        if not ids:
            print("No UNSEEN messages")
            return

        latest_id = ids[-1]
        status, msg_data = imap.fetch(latest_id, "(RFC822)")
        if status != "OK":
            print("IMAP fetch failed:", status, msg_data)
            return

        raw = msg_data[0][1]
        msg = BytesParser(policy=default).parsebytes(raw)

        print("From:", msg.get("From"))
        print("To:", msg.get("To"))
        print("Subject:", msg.get("Subject"))
        print("Date:", msg.get("Date"))

        # Print first text/plain body part (if any)
        body_text = None
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body_text = part.get_content()
                    break
        else:
            if msg.get_content_type() == "text/plain":
                body_text = msg.get_content()

        if body_text is not None:
            print("\nBody (text/plain):\n", body_text)
        else:
            print("\nBody: (no text/plain part found)")

    finally:
        try:
            imap.close()
        except Exception:
            pass
        imap.logout()


if __name__ == "__main__":
    main()
