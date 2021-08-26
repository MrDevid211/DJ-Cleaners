import requests
from django.shortcuts import render, redirect
from .forms import CityListForm
from .models import CityList


def add_city(request):
    citys = CityList.objects.all() # Получаем города данны из таблички CityList
    error = '' # Шоб коду плохо не было создадим эту переменную заранее,а то ругается
    if request.method == "POST": # Проверяем что мы там вообще получаем и если это было кинуто через POST - продолжаем
        form = CityListForm(request.POST)  # Запихаем эти данные в переменную
        if form.is_valid(): # Проверяем на валидность (не напартачили ли со вводом)
            form.save() # Кидаем всё это в нашу табличку в БД

            # И кидаем нас обратно на страницу добавления. Тут даже поясню зачем ибо мы и так остаёмся на ней
            return redirect('/add_city')

        else:
            error = "Форма заполнена не верно"

    form = CityListForm
    # Ну тут мы просто пихаем наши байтики данных на страницу, где и уже сожно будет красивенько или не очень разместить
    context = {
        'form': form,
        'error': error,
        'citys': citys,
    }
    return render(request, 'city/add_city.html', context)

