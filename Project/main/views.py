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
        customer_phone_number = request.POST.getlist('select_customer')[0]
        time = date_time[11:] + ':00'
        date = date_time[:-6]

        dt = DT.datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M:%S')
        unix_time_start = int(dt.timestamp())


        cleaner_choice(unix_time_start,customer_phone_number)




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




def cleaner_choice(unix_time_start, customer_phone_number):
    print(unix_time_start)
    booking = Booking.objects.all()

    if len(booking) == 0: # Еслинаша таблица с бронированием пустая - не выдумываем и сразу кидаем туда данные
        busy_cleaners_id = [] # Создадим что бы не ругалось
        top_cleaners_quality, top_cleaners_id, top_cleaners_durations  = search_top_cleaner(busy_cleaners_id) # Получаем из функции поиска топ клинера нужные нам данные о клинере
        unix_time_end = unix_time_start + top_cleaners_durations

    else: # Но если нет
        top_cleaners_quality, top_cleaners_id, top_cleaners_durations  = check_DB(booking, unix_time_start)  # Запускаем седующую функцию, которая проверит все записи в таблице бронирования
        unix_time_end = unix_time_start + top_cleaners_durations

    # Аккуратно бросаем эти данные в табицу
    booking = Booking(customer_phone_number=customer_phone_number,
                      top_cleaners_id=top_cleaners_id,
                      top_cleaners_durations=top_cleaners_durations,
                      unix_time_start=unix_time_start,
                      unix_time_end=unix_time_end)

    booking.save()


def check_DB(booking, unix_time_start):

    for note in booking: # Перебираем все записи
        start_t = note.unix_time_start
        finish_t = note.unix_time_end
        ids = note.top_cleaners_id
        busy_cleaners_id = outside(unix_time_start, start_t, finish_t, ids) # Запускаем функцию, которая проверит кто из клинеров занят на нужное время

        top_cleaners_quality, top_cleaners_id, top_cleaners_durations  = search_top_cleaner(busy_cleaners_id) # Кидаем в нашу функцию поиска топ клинера список клинеров,что заняты

        return top_cleaners_quality, top_cleaners_id, top_cleaners_durations

def outside(unix_time_start, start_t, finish_t, ids): # Принимаем время, на которое нужен клинер, время начала клининга в очереднй записи и время конца клининга этой же записи
    busy_cleaners_id = [] # Список id клинеров, что заняты на нужное время, который мы кинем дальше что бы знать, кто занят и кого не трогать
    if start_t > unix_time_start and start_t < finish_t:
        busy_cleaners_id.append(ids)
    return  busy_cleaners_id



def search_top_cleaner(busy_cleaners_id):
    cleaners = Cleaner.objects.all()
    quality_score_cleaners = {}
    id_n_durations = {}
    for i in cleaners:
        if i.id in busy_cleaners_id:
            continue
        else:
            id_n_durations[i.id] = i.duration
            quality_score_cleaners[float(i.quality_score)] = i.id

    top_cleaners_quality = max(quality_score_cleaners)
    top_cleaners_id = quality_score_cleaners[top_cleaners_quality]
    top_cleaners_durations = (id_n_durations[top_cleaners_id])*60
    print(top_cleaners_quality)
    print(top_cleaners_id)
    print(top_cleaners_durations)

    return top_cleaners_quality, top_cleaners_id, top_cleaners_durations