import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_message(sender_email, receiver_emails, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)
    message["Subject"] = subject
    message["Bcc"] = ", ".join(receiver_emails)
    message.attach(MIMEText(body, "plain"))
    return message


def attach_file(message, filename):
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    message.attach(part)
    return message


def send_email(sender_email, receiver_emails, password, message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, message.as_string())


# Define email configuration
subject = "transcribed text from your meeting"
body = "This is the transcribed text from your meeting"
sender_email = "hyeshesh@gmail.com"
receiver_emails = ["hyesheshnath@gmail.com", "hysheshnath@gmail.com", "salilaps7@gmail.com"]
password = "axvctkoqcikcvpmp"
filename = "output_en.txt"

# Create message
message = create_message(sender_email, receiver_emails, subject, body)

# Attach file
message = attach_file(message, filename)

# Send email
send_email(sender_email, receiver_emails, password, message)
