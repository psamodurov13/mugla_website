from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import *
# Create your views here.


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['processed'] = False
            form_data.pop('captcha')
            new_message = FeedbackMessage.objects.create(**form_data)
            new_message.save()
            messages.success(request, 'Сообщение отправлено')
            return redirect('feedback')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/index.html', {'form': form})
