from celery import shared_task
import time

from .email_sending import mass_email_sending, send_email_about_post

# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")

@shared_task
def task_mass_email_sending():
    mass_email_sending()

@shared_task
def task_send_email_about_post(post_id):
    send_email_about_post(post_id)
