from .models import Cleaner
from django.forms import ModelForm, TextInput, Textarea


class CleanerForm(ModelForm):
    class Meta:
        model = Cleaner
        fields = [ "city","other_city"]
        widgets = {
            'city': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Введите название',
            }),
            'other_city': Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Введите задачу'
            }),
        }