import smtplib
import os
import ssl
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

PASSWORD=os.getenv("PASSWORD")
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587 

sender="jenna.jaehnig@gmail.com"
receiver="jjaehnig@umich.edu"

def send_email(clinician_id, msg_type, erorr_msg=None):
    if msg_type == "out_of_range":
        text=f"clinician_id {clinician_id} is out of range"
    elif msg_type == "error":
        text=f"Fetching clinician_id {clinician_id} encountered an error: {erorr_msg}"
    message = MIMEText(text, "plain")
    message["Subject"] = "Clinician Out of Range Alert"
    message["From"] = sender
    message["To"] = receiver
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(sender, PASSWORD)
            server.sendmail(sender, receiver, message.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")