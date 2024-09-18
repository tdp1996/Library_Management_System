from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search for books', max_length=100)

class SignUpForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['Member_Name', 'Email', 'Phone', 'Member_Address']
