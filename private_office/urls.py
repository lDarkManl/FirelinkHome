from django.urls import path
from . import views

app_name = 'private_office'
urlpatterns = [
	path('register/', views.registration, name = 'registration'),
	path('login/', views.user_login, name = 'login'),
	path('logout/', views.user_logout, name = 'logout'),
	path('private_office/', views.private_office, name = 'private_office'),
	path('set_name/', views.set_name, name = 'set_name'),
	path('set_image/', views.set_image, name = 'set_image'),
]