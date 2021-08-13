import datetime as DT

from django.shortcuts import render, redirect

from cleaners.models import Cleaner
from customers.models import Customer

from .forms import BookingForm
from .models import Booking


def home(request):

    customers = Customer.objects.all()

    error = ''  # Шоб коду плохо не было создадим эту переменную заранее,а то ругается
    if request.method == "POST":  # Проверяем что мы там вообще получаем и если это было кинуто нам через POST (не церковный) - продолжаем

        date_time = request.POST.getlist('date_time')[0] #
        user_phone = request.POST.getlist('select_customer')[0]
        time = date_time[11:] + ':00'
        date = date_time[:-6]

        dt = DT.datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M:%S')
        unix_time_start = dt.timestamp()


        cleaner_choice(unix_time_start)




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


def cleaner_choice(unix_time_start):
    print(unix_time_start)

    booking = Booking.objects.all()
#
#     for note in booking:
#         start_t = note.unix_time_start
#         finish_t = note.unix_time_end
#         check = outside(unix_time_start, start_t, finish_t)
#         print(type(check))
#         if check:
#             print(1111)
#
# def outside(unix_time_start, start_t, finish_t):
#     print(222)
#     if start_t > unix_time_start and start_t < finish_t:
#         return False
#     else:
#         return True
#




    cleaners = Cleaner.objects.all()
    quality_score_cleaners = {}
    id_n_durations = {}
    for i in cleaners:
        id_n_durations[i.id] = i.duration
        quality_score_cleaners[float(i.quality_score)] = i.id

    top_cleaners_quality = max(quality_score_cleaners)
    top_cleaners_id = quality_score_cleaners[top_cleaners_quality]
    top_cleaners_durations = id_n_durations[top_cleaners_id]
    print(top_cleaners_quality)
    print(top_cleaners_id)
    print(top_cleaners_durations*60)