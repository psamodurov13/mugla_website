from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView
# Create your views here.
from mugla_site.tasks import send_email_to_user
from subscription.forms import SubscriptionForm
from subscription.models import Subscription
from mugla_site.settings import FROM_EMAIL, ADMIN_EMAIL


class SubscriptionView(CreateView):
    model = Subscription
    form_class = SubscriptionForm

    def form_valid(self, form):
        # Формируем сообщение для отправки
        print('valid')
        data = form.data
        content = f'Вы успешно подписаны на новости'
        email = data['email']
        send_email_to_user.delay(email, 'Подписка на новости', content)
        send_email_to_user.delay(ADMIN_EMAIL, 'Новый подписчик', f'Новый подписчик - {data["name"]}, {email}')
        print(self.request.__dict__['META']['HTTP_REFERER'])
        messages.success(self.request, 'Вы успешно подписались на новости')
        return super().form_valid(form)

    def get_success_url(self):
        current_page = self.request.__dict__['META']['HTTP_REFERER'].replace(
            self.request.__dict__['META']['HTTP_ORIGIN'], '')
        return current_page

    def form_invalid(self, form):
        errors = form.errors.get_json_data(escape_html=False).values()
        for i in errors:
            messages.error(self.request, i[0]['message'])
        return HttpResponseRedirect(self.request.__dict__['META']['HTTP_REFERER'].replace(
            self.request.__dict__['META']['HTTP_ORIGIN'], ''))


