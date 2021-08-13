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
    citys = CityList.objects.all()
    cleaner = Cleaner.objects.all() # Получаем байтики данны из таблички CityList
    error = '' # Шоб коду плохо не было создадим эту переменную заранее,а то ругается
    if request.method == "POST": # Проверяем что мы там вообще получаем и если это было кинуто нам через POST (не церковный) - продолжаем

        citylist = request.POST.getlist('other_city')
        main_city = request.POST.getlist('main_city')


        form = CleanerForm(request.POST, request.POST.getlist('other_city'))  # Запихаем эти данные в переменную

        if form.is_valid(): # Проверяем на валидность (не напартачили ли со вводом)
            form.save() # Кидаем всё это в нашу табличку в БД

            # ВНИМАНИЕ! AHTUNG! УВАГА!
            # Ниже находятся костыли
            city_for_details = ', '.join(citylist) # Делаем из списка строку с городами

            Cleaner.objects.filter(city='1').update(city=main_city[0]) # Ну тут мы точечно меняем запист в БД и пихаем туда наши данные
            Cleaner.objects.filter(other_city='2').update(other_city=citylist) # Тут тоже
            Cleaner.objects.filter(other_city_for_details='3').update(other_city_for_details=city_for_details) # И тут (да ну, серьёзно?)

            return redirect('/cleaners/new')
        else:
            error = "Форма заполнена не верно"

    form = CleanerForm
    # Ну тут мы просто пихаем наши байтики данных на страницу, где их уже можно будет красивенько (или не очень) разместить
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