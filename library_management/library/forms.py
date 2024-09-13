from django import forms

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search for books', max_length=100)
