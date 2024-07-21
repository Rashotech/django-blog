from django.db import models
from django.contrib.auth.models import User
from django import forms

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Make the username and email fields read-only
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
