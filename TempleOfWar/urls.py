from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from . import views
from . import sitemap as user_sitemap
sitemaps = {
    'articles': user_sitemap.ArticleSitemap,
    'music': user_sitemap.TrackSitemap,
    'arts': user_sitemap.ArtSitemap,
    'static': user_sitemap.StaticSitemap
}

urlpatterns = [
    path('121322313212321312213/', admin.site.urls),
    path('', views.index, name='index'),
    path('search/', include(('search.urls'), namespace='search')),
    path('articles/', include(('articles.urls'), namespace='articles')),
    path('arts/', include(('arts.urls'), namespace='arts')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('music/', include(('music.urls'), namespace='music')),
    path('private_office/', include(('private_office.urls'), namespace='private_office')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.pageNotFound