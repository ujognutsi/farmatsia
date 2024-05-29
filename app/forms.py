from django import forms
from django.core.exceptions import ValidationError
from app.models import CustomUser
from django.db import models

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        if self.cleaned_data['username'] != self.cleaned_data['password']:
            raise ValidationError('Login and password don\'t match!')
            print('soemethi')
        
class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['login', 'password', 'avatar']

    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField()
    
    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Passwords don\'t match!')
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    # commit = False - вызываем метод, но в базе не сохраняем
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user