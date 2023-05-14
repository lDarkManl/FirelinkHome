from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Profile

class UserRegistrationForm(UserCreationForm):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Имя пользователя'}))
	password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Пароль'}))
	password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Подтверждение пароля'}))
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Имя пользователя'}))
	password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Пароль'}))

class UserForm(forms.ModelForm):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Имя пользователя'}))
	class Meta:
		model = User
		fields = ['username']


class ProfileForm(forms.ModelForm):
	image = forms.FileField(label='', widget=forms.FileInput(attrs={'class':'form-control bg-dark text-light form-control-sm', 'id':'formFileSm'}))
	class Meta:
		model = Profile
		fields = ['image']
