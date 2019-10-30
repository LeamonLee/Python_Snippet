import os
import smtplib          # python built-in module
import requests
# import logging
from linode_api4 import LinodeClient, Instance

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')

# logging.basicConfig(filename='PATH_TO_DESIRED_LOG_FILE',
#                     level=logging.INFO,
#                     format='%(asctime)s:%(levelname)s:%(message)s')


def notify_user():
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()         # Identify ourself with the mail server that we're using
        smtp.starttls()     # Encrypt our traffic
        smtp.ehlo()         # Reidentify ourself as an encrypted connection

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = 'YOUR SITE IS DOWN!'
        body = 'Make sure the server restarted and it is back up'
        msg = f'Subject: {subject}\n\n{body}'

        # logging.info('Sending Email...')
        
        # smtp.sendmail(SENDER, RECEIVER, MSG) 
        smtp.sendmail(EMAIL_ADDRESS, 'INSERT_RECEIVER_ADDRESS', msg)


def reboot_server():
    client = LinodeClient(LINODE_TOKEN)

    # Print out all of the instances on the linode server
    # for my_linode in client.linode_api4.instances():
    #     print(f"{linode.label}: {linode.id}")
    
    my_server = client.load(Instance, 376715)
    my_server.reboot()
    # logging.info('Attempting to reboot server...')


try:
    # Requests library will wait indefinitely if the server is no response.
    # So need to set the timeout
    # If the server is down, or timeout happens, it's gonna throw an exception instead of keepping executing the following code. 
    r = requests.get('https://example.com', timeout=5)

    if r.status_code != 200:
        # logging.info('Website is DOWN!')
        notify_user()
        reboot_server()
    else:
        # logging.info('Website is UP')
except Exception as e:
    # logging.info('Website is DOWN!')
    notify_user()
    reboot_server()