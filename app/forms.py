from django import forms

class ContactForm(forms.Form):
    query = forms.CharField()