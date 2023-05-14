from django.contrib import admin
from .models import Track, Comment
from django.utils.safestring import mark_safe

class TrackAdmin(admin.ModelAdmin):
	list_display = ('id', 'author', 'track_title', 'get_photo')
	list_display_links = ('id', 'author', 'track_title')
	search_fields = ('author__username', 'track_title')
	
	def get_photo(self, object):
		if object.image:
			return mark_safe(f'<img src="{object.image.url}" alt="" width="100px">')
	get_photo.short_description = 'Изображение'


admin.site.register(Track, TrackAdmin)
admin.site.register(Comment)
