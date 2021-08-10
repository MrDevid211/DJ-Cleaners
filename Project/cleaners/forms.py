from .models import Cleaner
from django.forms import ModelForm, TextInput, Textarea


class CleanerForm(ModelForm):
    class Meta:
        model = Cleaner
        fields = ['first_name', 'last_name', 'quality_score', "duration", "city","other_city"]
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Введите имя',
            }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Введите фамилию'
            }),
            'quality_score': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Введите рейтинг клинера',
            }),
            'duration': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Введите время клининга'
            }),
        }