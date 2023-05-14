from django.shortcuts import render, reverse
from articles.models import Article
from arts.models import Art
from music.models import Track
from django.http import HttpResponseNotFound

def index(request):
	new_articles_list = Article.objects.filter(is_published=True).order_by('-update_date')[:9]
	new_article = new_articles_list[0]
	new_arts_list = Art.objects.order_by('-pub_date')[:5]
	new_tracks_list = Track.objects.order_by('-pub_date')[:5]
	return render(request, 'index.html', {'new_articles_list': new_articles_list[1:9], 'new_arts_list': new_arts_list, 'new_tracks_list': new_tracks_list, 'new_article': new_article})

def pageNotFound(request, exception):
	return HttpResponseNotFound('<h1 style="width:100%; text-align:center;">Страница не найдена</h1>')