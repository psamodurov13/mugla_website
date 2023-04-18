from celery import shared_task
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from mugla_site.celery import app

from mugla_site.utils import send, send_html_email
from collect_data.load import load_companies, res
from collect_data.collect import collect_data
from collect_data.models import CollectData


@app.task
def send_email_to_user(user_email, subject, text):
    send(user_email, subject, text)


@app.task
def send_html_email_to_user(user_email, subject, html_message):
    send_html_email(user_email, subject, html_message)


@app.task
def load_companies_task(url, city, query, id):
    try:
        res = collect_data(url, city)
        load_companies(res, query, city)
        obj = CollectData.objects.get(id=id)
        obj.collect_status = 'Выполнен'
        obj.save()
    except Exception:
        obj = CollectData.objects.get(id=id)
        obj.collect_status = 'Ошибка'
        obj.save()





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