import os
import smtplib
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

contacts = ['YourAddress@gmail.com', 'test@example.com']

msg = EmailMessage()
msg['Subject'] = 'Check out Bronx as a puppy!'
msg['From'] = EMAIL_ADDRESS

# If you want to send the email to multiple people at once.
# msg['To'] = contacts
# msg['To'] = ', '.join(contacts)

msg['To'] = 'YourAddress@gmail.com'
msg.set_content('This is a plain text email')


# Attached Files for images
attached_files = ["bronx_1.jpg", "bronx_2.jpg"]
for attached_file in attached_files:
    with open(attached_file, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)

# Attached Files for pdf
attached_files = ["sample.pdf"]
for attached_file in attached_files:
    with open(attached_file, 'rb') as f:
        file_data = f.read()
        file_name = f.name
    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)


msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">This is an HTML Email!</h1>
    </body>
</html>
""", subtype='html')


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)


# Plain old smtp
# with smtplib.SMTP("smtp.gmail.com", 587) as smtp2:
with smtplib.SMTP("localhost", 1025) as smtp2:              # The port on localhost is 1025

    # For gmail server or others. If we're using localhost one, then don't need to.
    # smtp2.ehlo()        # Identify ourselves with the mail server that we're using
    # smtp2.starttls()    # Encrypt our traffic
    # smtp2.ehlo()        # Reidentify ourselves as encrypted connection
    # smtp2.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    
    subject = "Grab dinner this weekend?"
    body = "How about dinner at 6pm this Saturday?"
    msg = f"Subject: {subject}\n\n{body}"

    # smtp2.sendmail(SENDER, RECEIVER, MESSAGE)
    smtp2.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, msg)