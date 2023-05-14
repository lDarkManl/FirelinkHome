from django.contrib import admin
from .models import Art, Comment, Tag
from django.utils.safestring import mark_safe

class ArtAdmin(admin.ModelAdmin):
	list_display = ('id', 'author', 'pub_date', 'get_photo')
	list_display_links = ('author',)
	search_fields = ('author',)
	def get_photo(self, object):
		if object.image:
			return mark_safe(f'<img src="{object.image.url}" alt="" width="100px">')
	get_photo.short_description = 'Изображение'

class TagAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	
admin.site.register(Art, ArtAdmin)
admin.site.register(Comment)
admin.site.register(Tag, TagAdmin)
