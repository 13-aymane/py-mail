import imaplib
import email

imap_server = ""
email_address =""
password = ""

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address,password)

imap.select("Inbox")

_,msgnums = imap.search(None, "ALL")

for msgnum in msgnum[0].split():
    _, data = imap.fetch(msgnum, "(RFC822")

    message = email.message_from_bytes(data[0][1])

    print(f"Message Number: {msgnum}")
    print(f"From: {message.get('From')}")
    print(f"To: {message.get('To')}")
    print(f"BCC: {message.get('BCC')}")
    print(f"Date: {message.get('Date')}")
    print(f"Subject: {message.get('From')}")

    print(f"Content:")
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            print(part.as_string())
imap.close()