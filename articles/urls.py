from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
	path('', views.index_articles, name = 'index'),
	path('<int:article_id>/', views.detail, name = 'detail'),
	path('category/<str:category_title>/', views.category, name = 'category'),
	path('game/', views.game, name = 'game'),
	path('category/<str:category_title>/game/', views.game_and_category, name = 'game_and_category'),
	path('<int:article_id>/comment', views.leave_comment, name = 'leave_comment'),
	path('comment/<int:article_id>/<int:comment_id>', views.delete_comment, name='delete_comment'),
	path('sub_comment/<int:article_id>/<int:sub_comment_id>', views.delete_comment, name='delete_sub_comment'),
	path('<int:article_id>/<int:comment_id>/comment', views.leave_comment, name = 'leave_sub_comment'),
	path('like/<int:article_id>', views.like, name = 'article_like'),
	path('like/<int:article_id>/<int:comment_id>', views.like, name = 'comment_like'),
]