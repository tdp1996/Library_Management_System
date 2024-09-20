from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Member

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search for books', max_length=100)

class SignUpForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['Member_Name', 'Email', 'Phone', 'Member_Address']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
