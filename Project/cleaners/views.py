from django.shortcuts import render, redirect
from django.urls import path, reverse_lazy
from django.forms import ModelForm, TextInput, Textarea
from .forms import CleanerForm
from city.forms import CityList

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
    print(333333333333333)
    citys = CityList.objects.all()
    cleaner = Cleaner.objects.all() # Получаем байтики данны из таблички CityList
    error = '' # Шоб коду плохо не было создадим эту переменную заранее,а то ругается
    if request.method == "POST": # Проверяем что мы там вообще получаем и если это было кинуто нам через POST (не церковный) - продолжаем
        form = CleanerForm(request.POST)  # Запихаем эти данные в переменную
        if form.is_valid(): # Проверяем на валидность (не напартачили ли со вводом)
            form.save() # Кидаем всё это в нашу табличку в БД
            #return redirect('/add_city')
            error = "Форма заполнена не верно"

    form = CleanerForm
    # Ну тут мы просто пихаем наши байтики данных на страницу, где и уже сожно будет красивенько или не очень разместить
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