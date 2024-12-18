from django import forms
from django.core.exceptions import ValidationError
from app.models import Profile, User, Answer
from django.db import models
from django.core.validators import validate_email

class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login', 'email', 'password', 'confirm_password', 'avatar']

    login = forms.CharField(min_length=5, max_length=20, required=True, label="Логин")
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    password = forms.CharField(min_length=6, max_length=32, required=True, widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(min_length=6, max_length=32, required=True, widget=forms.PasswordInput, label="Подтвердите пароль")
    avatar = forms.ImageField(required=False, label="Аватар (необязательно)")
    
    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Пароли не совпадают!')
        
    def init(self, *args, **kwargs):
        super(RegisterForm, self).init(*args, **kwargs)
        self.fields['avatar'].required = False

    def save(self, commit=True):
        lastId = User.objects.latest('id').id
        if not lastId:
            lastId = -1
        user = User.objects.create_user(id=lastId + 1, username=self.cleaned_data['login'], password=self.cleaned_data['password'], email=self.cleaned_data['email'])
        profile = Profile(id=lastId+1, user=user)
        if self.cleaned_data['avatar']:
            setattr(profile, 'avatar', self.cleaned_data['avatar'])
        profile.save()
        return user
    
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login', 'email']

    login = forms.CharField(min_length=5, max_length=20, required=True, label="Новый логин")
    email = forms.EmailField(required=True, widget=forms.EmailInput, label="Новая почта")
    
    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['login']
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    avatar = forms.ImageField(required=False, label="Новый аватар")
    
class QuestionForm(forms.Form):
    title = forms.CharField(min_length=10, max_length=255, required=True, label="Заголовок")
    text = forms.CharField(min_length=50, max_length=65535, required=True, label="Текст вопроса")
    tagsInput = forms.CharField(label="Тэги (необязательно)", help_text="Введите тэги, разделяя их запятыми")
    
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
    
    text = forms.CharField(label="Текст ответа")

class SearchForm(forms.Form):
    query = forms.CharField(label='', max_length=200)
