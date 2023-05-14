from ip.models import Ip
from django.contrib.contenttypes.models import ContentType

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR') # В REMOTE_ADDR значение айпи пользователя
    return ip

def add_view(request, obj):
	ip = get_client_ip(request)
	obj_type = ContentType.objects.get_for_model(obj)
	if not(Ip.objects.filter(ip=ip, content_type=obj_type, object_id=obj.id).exists()):
		ip_obj = Ip.objects.create(ip=ip, content_type=obj_type, object_id=obj.id)
		obj.views.add(ip_obj)