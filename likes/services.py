from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from .models import Like

def add_like(obj, user):
	obj_type = ContentType.objects.get_for_model(obj)
	Like.objects.create(content_type=obj_type, object_id=obj.id, user=user)

def delete_like(obj, user):
	obj_type = ContentType.objects.get_for_model(obj)
	Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()

def is_fan(obj, user):
	'''Проверка, поставил пользователь лайк или нет'''
	obj_type = ContentType.objects.get_for_model(obj)
	likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)
	return likes.exists()