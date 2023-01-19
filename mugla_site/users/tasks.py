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
