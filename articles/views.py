from django.shortcuts import render, reverse
from .models import Article, Game, Category, Comment, SubComment
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .forms import AddArticleForm, CommentForm, AddPhotoForm, SubCommentForm
from django.contrib import messages
from likes.services import *
from private_office.models import History
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ip.models import Ip
from django.contrib.contenttypes.models import ContentType
from ip.services import get_client_ip, add_view

def index_articles(request):
	'''Главная страница'''
	articles_list = Article.objects.filter(is_published=True).order_by('-update_date')
	games_list = Game.objects.order_by('pub_date')
	categories_list = Category.objects.order_by('pub_date')
	context = {'categories_list':categories_list, 'games_list': games_list, 'articles_list': articles_list}
	return render(request, 'articles/index_articles.html', context)

def detail(request, article_id):
	'''Страница статьи'''
	try:
		article = Article.objects.get(pk = article_id)
	except:
		raise Http404('Статья не найдена')

	user = False
	if request.user.is_authenticated:
		user = request.user
		if article.is_published == False and article.author != user:
			messages.error(request, 'Статья не найдена')
			return HttpResponseRedirect(reverse('articles:index'))
		History.objects.create(user=user, model='article', record_id=article_id)

	elif article.is_published == False:
		messages.error(request, 'Статья не найдена')
		return HttpResponseRedirect(reverse('articles:index'))

	add_view(request, article)
	
	games_list = Game.objects.order_by('pub_date')
	categories_list = Category.objects.order_by('pub_date')
	comments_list = Comment.objects.filter(article_id = article_id).order_by('-pub_date')
	form = CommentForm
	sub_form = SubCommentForm
	context = {'article': article, 'games_list': games_list, 'categories_list': categories_list, 'comments_list': comments_list, 'form': form, 'sub_form': sub_form, 'user': user}
	return render(request, 'articles/detail.html', context)

def category(request, category_title):
	'''Выбор по категории'''
	articles_list = Article.objects.filter(article_category__category_title_meta = category_title).order_by('-update_date')
	categories_list = Category.objects.order_by('pub_date')
	games_list = Game.objects.order_by('pub_date')
	category = Category.objects.get(category_title_meta = category_title)
	context = {'articles_list': articles_list, 'categories_list': categories_list, 'games_list': games_list, 'category_obj': category}
	return render(request, 'articles/category.html', context)

def game(request):
	'''Выбор по игре'''
	games = tuple(request.GET.getlist('game'))
	if games:
		articles_list = Article.objects.filter(article_game__game_title_meta__in = games, is_published=True).order_by('-update_date')
		categories_list = Category.objects.order_by('pub_date')
		games_list = Game.objects.order_by('pub_date')
		context = {'articles_list': articles_list, 'categories_list': categories_list, 'games_list': games_list, 'games': games}
		return render(request, 'articles/game.html', context)
	else:
		return HttpResponseRedirect(reverse('articles:index'))
	

def game_and_category(request, category_title):
	'''Выбор по игре и категории'''
	games = tuple(request.GET.getlist('game'))
	category = Category.objects.get(category_title_meta = category_title)
	if games:
		articles_list = Article.objects.filter(article_game__game_title_meta__in = games, article_category__category_title_meta = category_title).order_by('-update_date')
		categories_list = Category.objects.order_by('pub_date')
		games_list = Game.objects.order_by('pub_date')
		context = {'articles_list': articles_list, 'categories_list': categories_list, 'games_list': games_list, 'games': games, 'category_obj': category}
		return render(request, 'articles/game_and_category.html', context)
	else:
		return HttpResponseRedirect(reverse('articles:category', args=(category_title,)))

def leave_comment(request, article_id, comment_id=None):
	'''Сохраняет комментарий в БД и возвращает на detail'''
	if request.user.is_authenticated:
		if request.method == 'POST':
			if comment_id:
				form = SubCommentForm(request.POST)
				form.instance.comment_id = comment_id
				form.instance.author_id = request.user.id
				form.save()
			else:
				form = CommentForm(request.POST)
				form.instance.article_id = article_id
				form.instance.author_id = request.user.id
				form.save()
	else:
		messages.error(request, "Пожалуйста, зарегистрируйтесь для того, чтобы оставить комментарий")	
	return HttpResponseRedirect(reverse('articles:detail', args=(article_id,)))

def delete_comment(request, article_id, comment_id=None, sub_comment_id=None):
	'''Удалить комментарий'''
	try:
		if comment_id:
			comment = Comment.objects.get(pk=comment_id)
		if sub_comment_id:
			comment = SubComment.objects.get(pk=sub_comment_id)
	except Comment.DoesNotExist:
		messages.error(request, "Комментарий уже удален")
	else:
		if request.user == comment.author or request.user.is_admin:
			comment.delete()
		else:
			messages.error(request, "У вас нет прав на удаление этого комментария")
	return HttpResponseRedirect(reverse('articles:detail', args=(article_id,)))

def like(request, article_id, comment_id=None):
	'''Добавить или убрать лайк'''
	if request.user.is_authenticated:
		if comment_id:
			obj = Comment.objects.get(pk=comment_id)
		else:
			obj = Article.objects.get(pk=article_id)
		if is_fan(obj, request.user):
			delete_like(obj, request.user)
		else:
			add_like(obj, request.user)
	else:
		messages.error(request, 'Войдите, чтобы поставить оценку')
	return HttpResponseRedirect(reverse('articles:detail', args=(article_id,)))

