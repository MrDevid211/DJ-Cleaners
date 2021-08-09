from .models import CityList
from django.forms import ModelForm, TextInput, NumberInput

class CityListForm(ModelForm):
    class Meta:
        model = CityList
        fields = ["city", "price"]

        widgets = {"city": TextInput(attrs=({
            'class': 'form-control',
            'placeholder': "Введите название города",
            'pattern': "^[a-zA-Z]+$"
        })),
            "price": NumberInput(attrs=({
                'class': 'form-control',
                'placeholder': "Введите название города",
            }))
        }
