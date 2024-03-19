from django.contrib.sitemaps import Sitemap
from articles.models import Article
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

class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)
        
