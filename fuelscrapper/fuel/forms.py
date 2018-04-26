# -*- coding: utf-8 -*-
from django import forms

class Contact(forms.Form):
    name = forms.CharField(max_length = 50)
    email = forms.EmailField(max_length = 250, help_text='example@email.com')
    subject = forms.CharField(max_length = 250, help_text='Subject')
    message = forms.CharField(max_length = 2000, widget = forms.Textarea(), help_text='Write your message here')
    
    # hidden input to inform which page the user send the message
    source = forms.CharField(max_length= 50, widget=forms.HiddenInput())
    
    def clean_data(self):
        cleaned_data = super(Contact, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        subject = cleaned_data.get('subject')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')
            
# class FuelScrap(forms.Form):
    
