import requests
from django.shortcuts import render, redirect
from .forms import CityListForm


def add_city(request):
    error = ''
    if request.method == "POST":
        form = CityListForm(request.POST)
        if form.is_valid():
            form.save()
            
        else:
            error = "Форма заполнена не верно"


    form = CityListForm
    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'city/add_city.html', context)

