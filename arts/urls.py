from django.urls import path
from . import views

app_name = 'arts'
urlpatterns = [
	path('', views.index_arts, name = 'index'),
	path('<int:art_id>/', views.detail, name = 'detail'),
	path('<int:art_id>/comment', views.leave_comment, name = 'leave_comment'),
	path('<int:art_id>/<int:comment_id>/comment', views.leave_comment, name = 'leave_sub_comment'),
	path('comment/<int:art_id>/<int:comment_id>', views.delete_comment, name='delete_comment'),
	path('sub_comment/<int:art_id>/<int:sub_comment_id>', views.delete_comment, name='delete_sub_comment'),
	path('tag/', views.tag, name = 'tag'),
	path('tag/<slug:tag_slug>', views.tag, name = 'tag_slug'),
	path('like/<int:art_id>', views.like, name = 'art_like'),
	path('like/<int:art_id>/<int:comment_id>', views.like, name = 'comment_like'),
	path('add_art', views.add_art, name = 'add_art'),
	path('delete_art/<int:art_id>', views.delete_art, name='delete_art'),
]