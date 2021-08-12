
from django.shortcuts import render, redirect

from customers.models import Customer
from .forms import BookingForm



def home(request):

    customers = Customer.objects.all()

    error = ''  # Шоб коду плохо не было создадим эту переменную заранее,а то ругается
    if request.method == "POST":  # Проверяем что мы там вообще получаем и если это было кинуто нам через POST (не церковный) - продолжаем

        date_time = request.POST.getlist('date_time')[0] #
        user_phone = request.POST.getlist('select_customer')[0]
        time = date_time[11:]
        date = date_time[:-6]
        print(time, date, user_phone)

        form = BookingForm(request.POST)  # Запихаем эти данные в переменную

        if form.is_valid():  # Проверяем на валидность (не напартачили ли со вводом)
            #form.save()  # Кидаем всё это в нашу табличку в БД

            return redirect('/')
        else:
            error = "Форма заполнена не верно"

    form = BookingForm
    # Ну тут мы просто пихаем наши байтики данных на страницу, где их уже можно будет красивенько (или не очень) разместить
    context = {
        'form': form,
        'error': error,
        'customers': customers,
    }

    return render(request, 'main/home.html', context)
