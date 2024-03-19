from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserLoginForm, UserForm, ProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import History
from articles.models import Article
from django.db.models import When, Case
from django.contrib.contenttypes.models import ContentType

def registration(request):
	'''Регистрация'''
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Регистрация успешно завершена')
			return HttpResponseRedirect(reverse('private_office:private_office'))
		else:
			messages.error(request, 'Ошибка регистрации')
	else:
		form = UserRegistrationForm()
	context = {'form': form}
	return render(request, 'private_office/registration.html', context)

def user_login(request):
	'''Войти в аккаунт'''
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return HttpResponseRedirect(reverse('private_office:private_office'))
		else:
			messages.error(request, 'Ошибка входа')
	else:
		form = UserLoginForm()
	context = {'form': form}
	return render(request, 'private_office/login.html', context)

def private_office(request):
	'''Личный кабинет'''
	if request.user.is_authenticated:
		photo_form = ProfileForm()
		user_form = UserForm()
		history = History.objects.filter(user=request.user).order_by('-date')
		articles_list = get_history(history, 'article')
		user_articles_list = Article.objects.filter(author=request.user).order_by('-pub_date')
		return render(request, 'private_office/private_office.html', {'photo_form': photo_form, 'user_form':user_form, 'articles_list': articles_list})
	return HttpResponseRedirect(reverse('private_office:login'))

def get_history(history, model, count=None):
	'''Получить историю по модели'''
	id_post = []
	for record in history:
		if record.model == model:
			id_post += [record.record_id]
	order_posts = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(id_post)])
	content_type = ContentType.objects.get(model=model)
	Model = content_type.model_class()
	posts_list = Model.objects.filter(pk__in=id_post).order_by(order_posts)
	if count:
		posts_list = posts_list[:count]
	return posts_list

def set_name(request):
	'''Установить имя'''
	if request.user.is_authenticated:
		if request.method == 'POST':
			user_form = UserForm(request.POST, instance=request.user)
			if user_form.is_valid():
				user_form.save()
			messages.success(request, 'Ваш профиль был успешно обновлен!')
			return HttpResponseRedirect(reverse('private_office:private_office'))
	else:
		return HttpResponseRedirect(reverse('private_office:login'))

def set_image(request):
	'''Установить изображение'''
	if request.user.is_authenticated:
		if request.method == 'POST':
			profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
			if profile_form.is_valid():
				profile_form.save()
				messages.success(request, 'Фото успешно сменено')
			else:
				messages.error(request, 'Ошибка')
		return HttpResponseRedirect(reverse('private_office:private_office'))
	else:
		return HttpResponseRedirect(reverse('private_office:login'))

def user_logout(request):
	'''Выйти из аккаунта'''
	logout(request)
	return HttpResponseRedirect(reverse('private_office:login'))
