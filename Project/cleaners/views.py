from django.shortcuts import render, redirect
from django.urls import path, reverse_lazy
from django.forms import ModelForm, TextInput, Textarea
from .forms import CleanerForm
from city.forms import CityList
from city.forms import CityListForm

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Cleaner


class CleanerList(ListView):
    model = Cleaner


class CleanerDetail(DetailView):
    model = Cleaner


def CleanerCreation(request):
    citys = CityList.objects.all() # Получаем список городов
    cleaner = Cleaner.objects.all() # Получаем байтики данны из таблички CityList
    error = '' # Шоб коду плохо не было создадим эту переменную заранее,а то ругается
    if request.method == "POST": # Проверяем что мы там вообще получаем и если это было кинуто через POST - продолжаем

        citylist = request.POST.getlist('other_city')
        main_city = request.POST.getlist('main_city')

        form = CleanerForm(request.POST, request.POST.getlist('other_city'))  # Запихаем эти данные в переменную

        if form.is_valid(): # Проверяем на валидность (не напартачили ли со вводом)
            form.save() # Кидаем всё это в нашу табличку в БД

            # Ну тут мы точечно меняем запист в БД и пихаем туда наши данные
            Cleaner.objects.filter(city='1').update(city=main_city[0])

            cleaner = Cleaner.objects.last()
            for city in citylist:
                city = CityList.objects.filter(city=city)
                print(type(city[0]))
                cleaner.other_city.add(city[0])

            return redirect('/cleaners/new')
        else:
            error = "Форма заполнена не верно"

    form = CleanerForm
    # Ну тут мы просто пихаем наши байтики данных на страницу
    context = {
        'form': form,
        'error': error,
        'cleaner': cleaner,
        'citys': citys,
    }

    return render(request, 'cleaners/cleaner_form.html', context)


class CleanerUpdate(UpdateView):

    model = Cleaner
    success_url = reverse_lazy('cleaners:list')
    fields = ['first_name', 'last_name', 'quality_score']


class CleanerDelete(DeleteView):
    model = Cleaner
    success_url = reverse_lazy('cleaners:list')