from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, ModelForm

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': "ad soyad"}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': "email"}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': "ad"}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': "asoyad"}),
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Kocaeli', 'Kocaeli')
]


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile  # model
        fields = ['phone', 'address', 'city', 'county', 'image']
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': "Telefon no"}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': "Adres"}),
            'city': Select(attrs={'class': 'input', 'placeholder': "Sehir"}, choices=CITY),
            'county': TextInput(attrs={'class': 'input', 'placeholder': "county"}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': "Image"}),
        }
