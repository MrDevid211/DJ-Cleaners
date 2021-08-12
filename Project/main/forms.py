from .models import Booking
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput




class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = []
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Введите имя',
            }),

        }