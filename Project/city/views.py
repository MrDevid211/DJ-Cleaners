from django.shortcuts import render



def add_city(request):
    return render(request, 'city/add_city.html')

