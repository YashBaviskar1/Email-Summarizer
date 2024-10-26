import time
from itertools import chain
import email
import imaplib
import os 
from PyPDF2 import PdfReader
from summarizer import summarize_email
imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'baymaxbots@gmail.com'
password = 'zbvy fash octd iwii'
from PyPDF2 import PdfReader
from summarizer import summarize_email
criteria = {}
uid_max = 0
download_folder = "attachments"  

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [('UID', '%d:*' % (uid_max + 1))]
    return '(%s)' % ' '.join(chain(*c))

def fetch_latest_email():
    global uid_max
    
    # Login to the IMAP server
    mail = imaplib.IMAP4_SSL(imap_ssl_host)
    mail.login(username, password)
    
    mail.select('inbox')
    result, data = mail.uid('SEARCH', None, search_string(uid_max, criteria))
    uids = [int(s) for s in data[0].split()]
    
    if uids:
        new_uid_max = max(uids)
        if new_uid_max > uid_max:
            uid_max = new_uid_max
            print("New Email UID:", uid_max)
            result, data = mail.uid('FETCH', str(uid_max), '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    email_msg = email.message_from_bytes(response_part[1])
                    
                    print("New Email Subject:", email_msg['subject'])
                    print("From:", email_msg['from'])
                    print("To:", email_msg['to'])
                    print("Date:", email_msg['date'])  

                    for part in email_msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if part.get_content_maintype() == 'multipart':
                            continue  

                        if part.get('Content-Disposition') is not None:
  
                            if content_disposition and 'attachment' in content_disposition:
                                file_name = part.get_filename()
                                if file_name and file_name.endswith('.pdf'):
                                    file_path = os.path.join(download_folder, file_name)
                                    with open(file_path, 'wb') as f:
                                        f.write(part.get_payload(decode=True))
                                    print(f"Downloaded attachment: {file_name}")
                                    reader = PdfReader(file_path)
                                    text = " "
                                    for page in reader.pages :
                                        text += page.extract_text()
                                    pdf_text_summary = summarize_email(text)
                                    print(f"Summary of the Attachment pdf :{pdf_text_summary}")
                            else : 
                                print("No attachments in this mail ")
                        else :
                            print("No attachments in this mail ")
    else:
        print("No new emails.")
        return None

    mail.logout()

fetch_latest_email()
