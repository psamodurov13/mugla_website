from celery import shared_task
from django.contrib.auth.models import User

from mugla_site.celery import app

from mugla_site.utils import send

@app.task
def send_email_registration(user_email, subject, text):
    send(user_email, subject, text)


@app.task
def send_beat_email():
    for user in User.objects.all():
        send(user.email, 'beat email', 'text')


@app.task
def my_task(a, b):
    c = a + b
    return c


@app.task(bind=True, default_retry_delay=5 * 60)
def my_task_retry(self, x, y):
    try:
        return x + y
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task()
def my_sh_task(msg):
    return msg + 'in a bottle'