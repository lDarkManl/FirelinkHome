from django.shortcuts import render, reverse
from .models import Art, Comment, Tag, SubComment
from .forms import CommentForm, AddArtForm, SubCommentForm
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from likes.services import *
from private_office.models import History
from django.contrib.contenttypes.models import ContentType
from ip.services import get_client_ip, add_view

def index_arts(request):
	arts_list = Art.objects.order_by('-pub_date')
	tags_list = Tag.objects.all()
	context = {'arts_list': arts_list, 'tags_list': tags_list}
	return render(request, 'arts/index_arts.html', context)

def detail(request, art_id):
	try:
		art = Art.objects.get(pk=art_id)
	except:
		raise Http404('Арт не найден')
	user = False
	if request.user.is_authenticated:
		user = request.user
		History.objects.create(user=user, model='art', record_id=art_id)
	add_view(request, art)
	comments_list = Comment.objects.filter(art_id=art_id)
	form = CommentForm()
	sub_form = SubCommentForm()
	context = {'art': art, 'comments_list':comments_list, 'form':form, 'sub_form': sub_form, 'user': user}
	return render(request, 'arts/detail.html', context)


def leave_comment(request, art_id, comment_id=None):
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
				form.instance.art_id = art_id
				form.instance.author_id = request.user.id
				form.save()
	else:
		messages.error(request, "Пожалуйста, зарегистрируйтесь для того, чтобы оставить комментарий")	
	return HttpResponseRedirect(reverse('arts:detail', args=(art_id,)))

def delete_comment(request, art_id, comment_id=None, sub_comment_id=None):
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
	return HttpResponseRedirect(reverse('arts:detail', args=(art_id,)))

def tag(request, tag_slug = None):
	arts_list = Art.objects.order_by('-pub_date')
	tag_values = tuple(request.GET.getlist('tag'))
	tag_search = request.GET.get('tag_search')
	tag_obj = None
	if tag_search:
		tag_search = tag_search.split(', ')
		tag_obj = Tag.objects.filter(name__in = tag_search)
	if tag_values:
		arts_list = Art.objects.filter(tags__slug__in = tag_values)
		tags_list = Tag.objects.all()
		selected_tags = Tag.objects.filter(slug__in = tag_values)
		context = {'arts_list': arts_list, 'tags_list':tags_list, 'selected_tags': selected_tags}
		return render(request, 'arts/tag.html', context)

	elif tag_slug:
		arts_list = Art.objects.filter(tags__slug__in = [tag_slug])
		tags_list = Tag.objects.all()
		selected_tags = Tag.objects.filter(slug__in = [tag_slug])
		context = {'arts_list': arts_list, 'tags_list':tags_list, 'selected_tags': selected_tags}
		return render(request, 'arts/tag.html', context)

	elif tag_obj:
		arts_list = Art.objects.filter(tags__slug__in = [tag.slug for tag in tag_obj])
		selected_tags = Tag.objects.filter(slug__in = [tag.slug for tag in tag_obj])
		tags_list = Tag.objects.all()
		context = {'arts_list': arts_list, 'tags_list':tags_list, 'selected_tags': selected_tags}
		return render(request, 'arts/tag.html', context)
	else:
		return HttpResponseRedirect(reverse('arts:index'))
	
def add_art(request):
	if request.user.is_staff:
		if request.method == 'POST':
			form = AddArtForm(request.POST, request.FILES)
			form.instance.author_id = request.user.id
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('arts:index'))
		else:
			form = AddArtForm()
			return render(request, 'arts/add_art.html', {'form': form})
	else:
		messages.error(request, 'Вы должны иметь статус персонала')
		return HttpResponseRedirect(reverse('index'))

def like(request, art_id, comment_id=None):
	if request.user.is_authenticated:
		if comment_id:
			obj = Comment.objects.get(pk=comment_id)
		else:
			obj = Art.objects.get(pk=art_id)
		if is_fan(obj, request.user):
			delete_like(obj, request.user)
		else:
			add_like(obj, request.user)
	else:
		messages.error(request, 'Войдите, чтобы поставить оценку')
	return HttpResponseRedirect(reverse('arts:detail', args=(art_id,)))
	
def delete_art(request, art_id):
	try: 
		art = Art.objects.get(pk=art_id)
	except:
		raise Http404('Not Found')
	art.delete()
	return HttpResponseRedirect(reverse('arts:index'))