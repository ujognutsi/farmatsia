from django import forms
from django.core.exceptions import ValidationError
from app.models import Profile, User
from django.db import models
from django.core.validators import validate_email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean(self):
    #     super().clean()
    #     if self.cleaned_data['username'] != self.cleaned_data['password']:
    #         raise ValidationError('Login and password don\'t match!')
        
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login', 'email', 'password', 'confirm_password', 'avatar']

    login = forms.CharField(min_length=5, max_length=20, required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    password = forms.CharField(min_length=6, max_length=32, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=6, max_length=32, required=True, widget=forms.PasswordInput)
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
        user = User.objects.create_user(username=self.cleaned_data['login'], password=self.cleaned_data['password'], email=self.cleaned_data['email'])
        # user = super().save(commit=False)
        profile = Profile(user=user)
        if self.cleaned_data['avatar']:
            setattr(profile, 'avatar', self.cleaned_data['avatar'])
        profile.save()
        # user.set_password(self.cleaned_data['password'])
        # user.save()
        return user
    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login', 'email', 'avatar']

    login = forms.CharField(min_length=5, max_length=20, required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    avatar = forms.ImageField()

    def save(self, commit=True):
        user = self.instance
        user.username = self.cleaned_data['login']
        user.email = self.cleaned_data['email']
        user.save()
        
        profile = user.profile
        profile.avatar = self.cleaned_data['avatar']
        profile.save()
        return user
    
class QuestionForm(forms.ModelForm):
    title = forms.CharField(min_length=10, max_length=255, required=True)
    text = forms.CharField(min_length=100, max_length=65535, required=True)
    # tagsInput = forms.CharField()

class AnswerForm(forms.ModelForm):
    text = forms.CharField(min_length=100, max_length=65535, required=True)