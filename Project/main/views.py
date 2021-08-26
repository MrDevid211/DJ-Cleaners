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
    if request.method == "POST":  # Проверяем что мы там вообще получаем и если это было кинуто через - продолжаем

        booking_city = request.POST.getlist('booking_city')[0]
        date_time = request.POST.getlist('date_time')[0]  #

        customer_phone_number = request.POST.getlist('select_customer')[0]
        time = date_time[11:] + ':00'
        date = date_time[:-6]

        dt = DT.datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M:%S')
        unix_time_start = int(dt.timestamp())

        error = cleaner_choice(unix_time_start, customer_phone_number, booking_city)

        form = BookingForm(request.POST)  # Запихаем эти данные в переменную

        # Ну здесь, пожалуй, стоит точно рассказать что и как
        if form.is_valid() and error != None:  # Проверяем на валидность (не напартачили ли со вводом)
            finish_time = []  # Собираем в список время завершения всех чисток
            after_unix_time = []  # Сюда кидаем только те, что закончатся уже после того времени, на которое хотят заказать чистку
            difference_in_time = []  # Здесь мы кидаем разницу во времени между желаемым началом чистки и концами тех, что будут в будущем
            booking = Booking.objects.all()

            for note in booking:  # Перебираем и кидаем в первый список все даты конца чисток
                finish_time.append(note.unix_time_end)

            # Здесь мы заполняем второй список датами, что будут лишь после той, на которой желают заказать чистку
            for time in finish_time:
                if time > unix_time_start:
                    after_unix_time.append(time)
                else:
                    continue

            for time in after_unix_time:  # Заполняем третий список уже выше описаными данными
                difference_in_time.append(time - unix_time_start)

            # Здесь просто смотрим, когда следующий клинер освободится и делаем некоторые преобразования
            min_time = min(difference_in_time)
            next_time_cleaner = unix_time_start + min_time

            from datetime import datetime
            # Делаем из unix времени обычное
            next_time_cleaner = datetime.utcfromtimestamp(next_time_cleaner).strftime('%Y-%m-%d %H:%M')
            print(next_time_cleaner)

            error = "Следующий клинер освободится в: "+str(next_time_cleaner)  # Кидаем на вывод на нашей странице

        elif form.is_valid() and error == None:
            return redirect('/')

        else:
            error = "Форма заполнена не верно"

    form = BookingForm
    # Ну тут мы просто пихаем наши байтики данных на страницу
    context = {
        'form': form,
        'error': error,
        'customers': customers,
        'citys': citys,
    }

    return render(request, 'main/home.html', context)


def cleaner_choice(unix_time_start, customer_phone_number, booking_city):
    notation = False  # Если будет 1 (True) - мы делаем запись в таблице БД
    booking = Booking.objects.all()
    customers = Customer.objects.all()

    if len(booking) == 0:  # Если наша таблица с бронированием пустая - не выдумываем и сразу кидаем туда данные
        busy_cleaners_id = []  # Создадим что бы не ругалось
        # Получаем из функции поиска топ клинера нужные нам данные о клинере
        top_cleaners_quality, top_cleaners_id, top_cleaners_durations = search_top_cleaner(busy_cleaners_id, booking_city)
        unix_time_end = unix_time_start + top_cleaners_durations
        notation = True
    else:  # Но если нет и в ней уже есть записи
        if len(check_DB(booking, unix_time_start, booking_city)) == 3:
            # Запускаем седующую функцию, которая проверит все записи в таблице бронирования
            top_cleaners_quality, top_cleaners_id, top_cleaners_durations = check_DB(booking, unix_time_start, booking_city)
            unix_time_end = unix_time_start + top_cleaners_durations
            notation = True  # Говорим что можно сделать запись в таблицу БД
        else:
            error = check_DB(booking, unix_time_start, booking_city)
            return error
    if notation:
        print('Лучший найденый клинер: ', top_cleaners_id )

        for customer in customers:
            if customer.phone_number == customer_phone_number:
                quality_score = customer.quality_score

        new_quality_score = int(quality_score)+1
        Customer.objects.filter(phone_number=customer_phone_number).update(quality_score=new_quality_score)

        citys = CityList.objects.all()
        price = []
        for city in citys:
            if city.city == booking_city:
                price.append(city.price)
        price = int(price[0])
        price = (price*(100-new_quality_score))/100

        # Аккуратно бросаем эти данные в табицу
        booking = Booking(customer_phone_number=customer_phone_number,
                          top_cleaners_id=top_cleaners_id,
                          top_cleaners_durations=top_cleaners_durations,
                          unix_time_start=unix_time_start,
                          unix_time_end=unix_time_end,
                          city=booking_city,
                          price=price)

        booking.save()


def check_DB(booking, unix_time_start, booking_city):

    busy_cleaners_id = []  # Список id клинеров, что заняты на нужное время что бы знать, кто занят и кого не трогать
    for note in booking:  # Перебираем все записи
        start_t = note.unix_time_start
        finish_t = note.unix_time_end
        ids = note.top_cleaners_id

        # Запускаем функцию, которая проверит кто из клинеров занят на нужное время
        busy_cleaners_id = get_busy_cleaners(unix_time_start, start_t, finish_t, ids, busy_cleaners_id)

    if len(search_top_cleaner(busy_cleaners_id, booking_city)) == 3:

        # Кидаем в нашу функцию поиска топ клинера список клинеров,что заняты
        top_cleaners_quality, top_cleaners_id, top_cleaners_durations = search_top_cleaner(busy_cleaners_id, booking_city)
        return top_cleaners_quality, top_cleaners_id, top_cleaners_durations
    else:
        error = search_top_cleaner(busy_cleaners_id, booking_city)
        return error


def get_busy_cleaners(unix_time_start, start_t, finish_t, ids, busy_cleaners_id):
    if start_t <= unix_time_start:  # Да, мне пришлось сделать каскад но это из-за одной проблемы с кодом
        if unix_time_start <= finish_t:
            busy_cleaners_id.append(ids)
    return busy_cleaners_id


def search_top_cleaner(busy_cleaners_id, booking_city):

    cleaners = Cleaner.objects.all()  # Получаем список клинеров
    quality_score_cleaners = {}  # Здесь у нас будет словарь {рейтинг клинера: его АйДи}
    id_and_durations = {}  # Такой же словарь только с {АйДи: Время клининга}
    cleaner_can_go_to = []  # Города, в которые может поеать клинер

    for cleaner in cleaners:  # Перебираем всех клинеров
        city_list = cleaner.other_city.all()

        if cleaner.id in busy_cleaners_id:  # Если клинер уже в "Занятых клинерах" - смотрим клинеров дальше
            continue

        else:  # Если он не занят - смотрим что у него тут по рейтингу, АйДи и времени чистки

            for city in city_list:  # Заполняем список городов, в которых может работать клинер
                cleaner_can_go_to.append(city.city)

            if booking_city in cleaner_can_go_to:
                pass
            else:  # Если этот клинер не работает в городе, в котором заказали чистку - ищем другого
                cleaner_can_go_to.clear()  # Чистим список что бы закинуть туда данные другого клинера
                continue

            cleaner_can_go_to.clear()  # Чистим список что бы закинуть туда данные другого клинера

            id_and_durations[cleaner.id] = cleaner.duration
            quality_score_cleaners[float(cleaner.quality_score)] = cleaner.id
    if len(quality_score_cleaners) != 0:  # Если список клинеров, которые на нужное время свободны - выбираем топового

        top_cleaners_quality = max(quality_score_cleaners)
        top_cleaners_id = quality_score_cleaners[top_cleaners_quality]
        top_cleaners_durations = (id_and_durations[top_cleaners_id])*60

        return top_cleaners_quality, top_cleaners_id, top_cleaners_durations

    else:  # Если нет - говорим, что увы, у нас тут никого нет на нужное время

        error = "На это время все клинеры заняты"

        print("На это время все клинеры заняты")

        return error
