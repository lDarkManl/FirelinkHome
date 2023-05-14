from django.contrib.sitemaps import Sitemap
from articles.models import Article
from music.models import Track
from arts.models import Art
from django.shortcuts import reverse


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.update_date

    def location(self, item):
        return f'/articles/{item.id}/'

class TrackSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Track.objects.all()

    def lastmod(self, obj):
        return obj.pub_date

    def location(self, item):
        return f'/music/comments/{item.slug}/'

class ArtSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Art.objects.all()

    def lastmod(self, obj):
        return obj.pub_date

    def location(self, item):
        return f'/arts/{item.id}/'

class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)
        
