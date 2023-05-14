from django.shortcuts import render
from articles.models import Article
from music.models import Track
from arts.models import Art
from django.db.models import Q

def search(request):
	'''Поиск'''
	search_title = str(request.GET.get('q'))
	search_list = search_title.split()
	articles_list = Article.objects.filter(*[Q(article_title__icontains=word) for word in search_list], is_published = True).order_by('-update_date')
	tracks_list = Track.objects.filter(*[Q(track_title__icontains=word) for word in search_list]).order_by('-pub_date')
	arts_list = Art.objects.filter(*[Q(title__icontains=word) for word in search_list]).order_by('-pub_date')
	context = {'articles_list': articles_list, 'tracks_list': tracks_list, 'arts_list': arts_list, 'query':search_title}
	return render(request, 'search/search.html', context)
