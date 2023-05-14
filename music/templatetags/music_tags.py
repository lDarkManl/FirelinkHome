from django import template
from django.contrib.contenttypes.models import ContentType
from likes.models import Like
register = template.Library()

@register.simple_tag()
def is_fan(obj, user):
	obj_type = ContentType.objects.get_for_model(obj)
	likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)
	if likes.exists():
		return 'fa-solid fa-heart'
	else:
		return 'fa-regular fa-heart'