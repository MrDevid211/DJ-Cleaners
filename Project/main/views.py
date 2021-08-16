import datetime as DT

from django.shortcuts import render, redirect

from cleaners.models import Cleaner
from customers.models import Customer
from city.forms import CityList

from .forms import BookingForm
from .models import Booking


def home(request):
    citys = CityList.objects.all()
    customers = Customer.objects.all()

    error = ''  # Шоб коду плохо не было создадим эту переменную заранее,а то ругается
    if request.method == "POST":  # Проверяем что мы там вообще получаем и если это было кинуто нам через POST (не церковный) - продолжаем

        booking_city = request.POST.getlist('booking_city')[0]
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
        'citys': citys,
    }

    return render(request, 'main/home.html', context)




def cleaner_choice(unix_time_start, customer_phone_number):
    notation = False # Если будет 1 (True) - мы делаем запись в таблице БД
    booking = Booking.objects.all()

    if len(booking) == 0: # Если наша таблица с бронированием пустая - не выдумываем и сразу кидаем туда данные
        busy_cleaners_id = [] # Создадим что бы не ругалось
        top_cleaners_quality, top_cleaners_id, top_cleaners_durations  = search_top_cleaner(busy_cleaners_id) # Получаем из функции поиска топ клинера нужные нам данные о клинере
        unix_time_end = unix_time_start + top_cleaners_durations

    else: # Но если нет и в ней уже есть записи
        if len(check_DB(booking, unix_time_start)) == 3:
            top_cleaners_quality, top_cleaners_id, top_cleaners_durations  = check_DB(booking, unix_time_start)  # Запускаем седующую функцию, которая проверит все записи в таблице бронирования
            unix_time_end = unix_time_start + top_cleaners_durations
            notation = True
        else:
            error = check_DB(booking, unix_time_start)
    if notation:
        # Аккуратно бросаем эти данные в табицу
        booking = Booking(customer_phone_number=customer_phone_number,
                          top_cleaners_id=top_cleaners_id,
                          top_cleaners_durations=top_cleaners_durations,
                          unix_time_start=unix_time_start,
                          unix_time_end=unix_time_end)
        #print(unix_time_start, unix_time_end)
        booking.save()



def check_DB(booking, unix_time_start):

    busy_cleaners_id = []  # Список id клинеров, что заняты на нужное время, который мы кинем дальше что бы знать, кто занят и кого не трогать
    for note in booking: # Перебираем все записи
        start_t = note.unix_time_start
        finish_t = note.unix_time_end
        ids = note.top_cleaners_id

        busy_cleaners_id = outside(unix_time_start, start_t, finish_t, ids, busy_cleaners_id) # Запускаем функцию, которая проверит кто из клинеров занят на нужное время

    if len(search_top_cleaner(busy_cleaners_id)) == 3:
        top_cleaners_quality, top_cleaners_id, top_cleaners_durations  = search_top_cleaner(busy_cleaners_id) # Кидаем в нашу функцию поиска топ клинера список клинеров,что заняты
        return top_cleaners_quality, top_cleaners_id, top_cleaners_durations
    else:
        error = "На это время все клинеры заняты"
        print("На это время все клинеры заняты 2")
        return error

def outside(unix_time_start, start_t, finish_t, ids, busy_cleaners_id): # Принимаем время, на которое нужен клинер, время начала клининга в очереднй записи и время конца клининга этой же записи
    if start_t <= unix_time_start: # Да, мне пришлось сделать каскад но это из-за одной проблемы с кодом

        if unix_time_start <= finish_t:

            busy_cleaners_id.append(ids)
         #   print(start_t, unix_time_start, finish_t)
    print(busy_cleaners_id)
    return  busy_cleaners_id



def search_top_cleaner(busy_cleaners_id):
    print(busy_cleaners_id)
    cleaners = Cleaner.objects.all() # Получаем список клинеров
    quality_score_cleaners = {}  # Здесь у нас будет словарь {рейтинг клинера: его АйДи}
    id_and_durations = {} # Такой же словарь только с {АйДи: Время клининга}
    for cleaner in cleaners: # Перебираем всех клинеров
        if cleaner.id in busy_cleaners_id: # Если клинер уже в "Занятых клинерах" - ничего не делаем и смотрим клинеров дальше
            continue
        else: # Если он не занят - смотрим что у него тут по рейтингу, АйДи и времени чистки
            id_and_durations[cleaner.id] = cleaner.duration
            quality_score_cleaners[float(cleaner.quality_score)] = cleaner.id
        #print(id_and_durations)
    if len(quality_score_cleaners) != 0: # Если список с клинерами, которые на нужное время свободны - выбираем топового
        top_cleaners_quality = max(quality_score_cleaners)
        top_cleaners_id = quality_score_cleaners[top_cleaners_quality]
        top_cleaners_durations = (id_and_durations[top_cleaners_id])*60
        print(top_cleaners_id)

        return top_cleaners_quality, top_cleaners_id, top_cleaners_durations
    else: # Если нет - говорим, что увы, у нас тут никого нет на нужное время
        error = "На это время все клинеры заняты"

        print("На это время все клинеры заняты 1")

        return error