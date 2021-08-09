
from django.urls import path, reverse_lazy


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


class CleanerCreation(CreateView):
    model = Cleaner
    success_url = reverse_lazy('cleaners:list')
    fields = ['first_name', 'last_name', 'quality_score']


class CleanerUpdate(UpdateView):
    model = Cleaner
    success_url = reverse_lazy('cleaners:list')
    fields = ['first_name', 'last_name', 'quality_score']


class CleanerDelete(DeleteView):
    model = Cleaner
    success_url = reverse_lazy('cleaners:list')