from django.urls import path
from . import views

app_name = 'music'
urlpatterns = [
	path('', views.index_music, name = 'index'),
	path('comments/<slug:track_slug>/', views.comments, name = 'comments'),
	path('author/', views.author, name = 'author'),
	path('<slug:track_slug>/comment/<int:track_id>/', views.leave_comment, name = 'leave_comment'),
	path('<slug:track_slug>/comment/<int:track_id>/<int:comment_id>/', views.leave_comment, name = 'leave_sub_comment'),
	path('comment/<slug:track_slug>/<int:comment_id>', views.delete_comment, name='delete_comment'),
	path('sub_comment/<slug:track_slug>/<int:sub_comment_id>', views.delete_comment, name='delete_sub_comment'),
	path('like/<slug:track_slug>', views.like, name = 'track_like'),
	path('like/<slug:track_slug>/<int:comment_id>', views.like, name = 'comment_like'),
	path('add_track/', views.add_track, name = 'add_track'),
	path('delete_track/<slug:track_slug>', views.delete_track, name='delete_track')
]