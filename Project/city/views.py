import requests
from django.shortcuts import render, redirect
from .forms import CityListForm
from .models import CityList


def add_city(request):
    citys = CityList.objects.all()
    error = ''
    if request.method == "POST":
        form = CityListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/add_city')
        else:
            error = "Форма заполнена не верно"


    form = CityListForm
    context = {
        'form': form,
        'error': error,
        'citys': citys,
    }
    return render(request, 'city/add_city.html', context)

