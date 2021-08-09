from django.urls import reverse_lazy

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .models import Customer


class CustomerList(ListView):
    model = Customer


class CustomerDetail(DetailView):
    model = Customer


class CustomerCreation(CreateView):
    model = Customer
    success_url = reverse_lazy('customers:list')
    fields = ['first_name', 'last_name', 'phone_number']


class CustomerUpdate(UpdateView):
    model = Customer
    success_url = reverse_lazy('customers:list')
    fields = ['first_name', 'last_name', 'phone_number']


class CustomerDelete(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers:list')