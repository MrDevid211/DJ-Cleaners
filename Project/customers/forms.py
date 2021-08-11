from .models import Customer
from django.forms import ModelForm, TextInput


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', "phone_number"]
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Введите имя',
            }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Введите фамилию'
            }),
            'phone_number': TextInput(attrs={
                'class': "form-control",
                'placeholder': '(+) от 9 до 15 цифр ',
                'pattern': "[+][0-9]{9,15}"
            }),


        }