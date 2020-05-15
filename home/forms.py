from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from home.models import Calculate


class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100)
    catid = forms.IntegerField()


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='User Name :')
    email = forms.CharField(max_length=200, label='Email :')
    first_name = forms.CharField(max_length=100, help_text='First Name', label='First Name :')
    last_name = forms.CharField(max_length=100, help_text='Last Name', label='Last Name :')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

class Rezervasyon(forms.Form):
    date_start=forms.DateField()
    date_end = forms.DateField()
    day=forms.IntegerField()
    class Meta:
        model=Calculate
        fields=('date_start','date_end','day')