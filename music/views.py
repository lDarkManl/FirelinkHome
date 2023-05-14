from django.shortcuts import render, reverse
from .models import Track, Comment, SubComment
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from .forms import CommentForm, AddTrackForm, SubCommentForm
from likes.services import *
from django.contrib import messages
from private_office.models import History
from django.contrib.contenttypes.models import ContentType
from ip.services import get_client_ip, add_view

def index_music(request):
	tracks_list = Track.objects.order_by('-pub_date')
	authors_list = User.objects.all()
	context = {'tracks_list': tracks_list, 'authors_list': authors_list}
	return render(request, 'music/index_music.html', context)

def author(request):
	if request.method == 'GET':
		author = request.GET.get('author')
		tracks_list = Track.objects.filter(author__username__icontains = author).order_by('-pub_date')
		context = {'tracks_list': tracks_list, 'query': author}
		return render(request, 'music/index_music.html', context)

def comments(request, track_slug):
	try:
		track = Track.objects.get(slug = track_slug)
	except:
		raise Http404("Трек не найден")
	form = CommentForm
	sub_form = SubCommentForm
	user = False
	if request.user.is_authenticated:
		user = request.user
		History.objects.create(user=user, model='track', record_id=track.pk)
	add_view(request, track)
	comments_list = Comment.objects.filter(track__slug = track_slug)
	context = {'track': track, 'form': form, 'comments_list': comments_list, 'sub_form': sub_form, 'user': user}
	return render(request, 'music/comments.html', context)

def leave_comment(request, track_slug, track_id, comment_id=None):
	'''Сохраняет комментарий в БД и возвращает на comments'''
	if request.user.is_authenticated:
		if request.method == 'POST':
			if comment_id:
				form = SubCommentForm(request.POST)
				form.instance.comment_id = comment_id
				form.instance.author_id = request.user.id
				form.save()
			else:
				form = CommentForm(request.POST)
				form.instance.track_id = track_id
				form.instance.author_id = request.user.id
				form.save()
	else:
		messages.error(request, "Пожалуйста, зарегистрируйтесь для того, чтобы оставить комментарий")
	return HttpResponseRedirect(reverse('music:comments', args=(track_slug,)))

def delete_comment(request, track_slug, comment_id=None, sub_comment_id=None):
	try:
		if comment_id:
			comment = Comment.objects.get(pk=comment_id)
		if sub_comment_id:
			comment = SubComment.objects.get(pk=sub_comment_id)
	except Comment.DoesNotExist:
		messages.error(request, "Комментарий уже удален")
	else:
		if request.user == comment.author:
			comment.delete()
		else:
			messages.error(request, "У вас нет прав на удаление этого комментария")
	return HttpResponseRedirect(reverse('music:comments', args=(track_slug,)))


def add_track(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = AddTrackForm(request.POST, request.FILES)
			form.instance.author_id = request.user.id
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('music:index'))
			else:
				messages.error(request, form.errors.as_data())
				return render(request, 'music/add_track.html', {'form': form})
		else:
			form = AddTrackForm()
			return render(request, 'music/add_track.html', {'form': form})
	else:
		messages.error(request, 'Войдите в аккаунт для добавления трека')
		return HttpResponseRedirect(reverse('index'))

def like(request, track_slug, comment_id=None):
	if request.user.is_authenticated:
		if comment_id:
			obj = Comment.objects.get(pk=comment_id)
		else:
			obj = Track.objects.get(slug=track_slug)
		if is_fan(obj, request.user):
			delete_like(obj, request.user)
		else:
			add_like(obj, request.user)
	else:
		messages.error(request, 'Войдите, чтобы поставить оценку')
	return HttpResponseRedirect(reverse('music:comments', args=(track_slug,)))

def delete_track(request, track_slug):
	try:
		track = Track.objects.get(slug=track_slug)
	except:
		raise Http404('Not found')
	track.delete()
	return HttpResponseRedirect(reverse('music:index'))