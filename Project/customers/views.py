from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CustomerForm

from .models import Customer


class CustomerList(ListView):
    model = Customer


class CustomerDetail(DetailView):
    model = Customer


def customer_creation(request):
    customer = Customer.objects.all()
    error = '' # Шоб коду плохо не было создадим эту переменную заранее,а то ругается
    if request.method == "POST": # Проверяем что мы там вообще получаем и если это было кинуто через POST - продолжаем

        form = CustomerForm(request.POST)  # Запихаем эти данные в переменную

        if form.is_valid(): # Проверяем на валидность (не напартачили ли со вводом)
            form.save() # Кидаем всё это в нашу табличку в БД
            return redirect('/customers/new')
        else:
            error = "Форма заполнена не верно"

    form = CustomerForm
    # Ну тут мы просто пихаем наши байтики данных на страницу
    context = {
        'form': form,
        'error': error,
        'customer': customer,
    }

    return render(request, 'customers/customer_form.html', context)


class CustomerUpdate(UpdateView):
    model = Customer
    success_url = reverse_lazy('customers:list')
    fields = ['first_name', 'last_name', 'phone_number']


class CustomerDelete(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers:list')