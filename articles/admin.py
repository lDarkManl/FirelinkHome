from django.contrib import admin
from .models import Article, Game, Category, Comment, SubComment
from django.utils.safestring import mark_safe

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'article_title', 'pub_date', 'update_date', 'is_published', 'article_game', 'article_category', 'get_photo')
	list_display_links = ('article_title',)
	search_fields = ('article_title',)
	def get_photo(self, object):
		if object.article_image:
			return mark_safe(f'<img src="{object.article_image.url}" alt="" width="100px">')
	get_photo.short_description = 'Изображение'

admin.site.register(Article, ArticleAdmin)
admin.site.register(Game)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(SubComment)