import imaplib, email
from email.header import decode_header
gmail = "baymaxbots@gmail.com"
password = "zbvy fash octd iwii"

imap = imaplib.IMAP4_SSL("imap.gmail.com")

imap.login(gmail, password)
print(imap.list())
status, messages = imap.select("INBOX")

print(status)
print(messages)

messages = int(messages[0])

print(messages)

res, msg = imap.fetch(str(messages), "(RFC822)")

for response_part in msg:
    if isinstance(response_part, tuple):
        msg = email.message_from_bytes(response_part[1])


        subject, encoding = decode_header(msg["Subject"])[0]
        print(msg["FROM"])
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        print("Subject:", subject)
        if msg.is_multipart():

            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
 
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
 
                    print("Message:", body)
        else:
            # Extract content type of the email
            content_type = msg.get_content_type()
            body = msg.get_payload(decode=True).decode()
            if content_type == "text/plain":

                print("Message:", body)