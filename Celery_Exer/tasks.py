from celery import Celery
import time

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://127.0.0.1:6379/0')

@celery.task
def send_email(mail):
    print('sending mail to {0} ...'.format(mail['to']))
    time.sleep(2)
    print('mail sent.')
    return 'Send Successful!'

@celery.task
def add(x, y):
    return x + y

# run command "celery -A tasks worker --loglevel=info" in terminal.

if __name__ == "__main__":
    send_email.delay("example@gmail.com", "thisismytoken")