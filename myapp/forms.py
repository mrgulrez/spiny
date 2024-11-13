from django import forms
from .models import Car, CarImage

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['title', 'description', 'car_type', 'company', 'dealer']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
