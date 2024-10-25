import time
from itertools import chain
import email
import imaplib
from summarizer import summarize_email, extract_tasks_dynamic
imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'baymaxbots@gmail.com'
password = 'zbvy fash octd iwii'

criteria = {}
uid_max = 0
email_text = None
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
                    # print(email_msg)
                    print("New Email Subject:", email_msg['subject'])
                    print("From:", email_msg['from'])
                    print("To:", email_msg['to'])
                    print("Date:", email_msg['date'])  
                    email_text = None
                    for part in email_msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
        
                            body = part.get_payload(decode=True)
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            print(1)
                            print("Message:", body[0 : len(body)-2])
                            email_text = body.decode('utf-8').replace('\r', '').replace('\n', '').strip()
                        else:
                            content_type = email_msg.get_content_type()
                            body = email_msg.get_payload(decode=True)
                            if content_type == "text/plain":
                                print(2)
                                print("Message:", body)
                                email_text = body.decode('utf-8').replace('\r', '').replace('\n', '').strip()
                        if email_text : 
                            summarized_email_text = summarize_email(email_text)
                            print(f"\n\nSummarised Email is : {summarized_email_text}")
                            dynamic_tasks_list = summarized_email_text.split('.')
                            print("Dynamic Tasks to Complete:")
                            for task in dynamic_tasks_list:
                                print(f"- {task}")

    else:
        print("No new emails.")

    mail.logout()

if __name__ == "__main__":
    fetch_latest_email()