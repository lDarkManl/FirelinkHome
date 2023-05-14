from django.contrib import admin
from .models import Ip

class IpAdmin(admin.ModelAdmin):
	list_display = ('ip', 'content_type', 'object_id')
	list_display_links = ('ip', 'content_type')

admin.site.register(Ip, IpAdmin)