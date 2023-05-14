from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import Like
from ip.models import Ip
from services.services import slugify

class Track(models.Model):
	track_title = models.CharField('Название', max_length = 100, unique=True)
	track_title_seo = models.CharField('Название в поиске', max_length = 100, unique=True, blank=True)
	track = models.FileField('Запись трека', upload_to = 'music/%Y/%m/%d/')
	image = models.ImageField('Изображение', upload_to = 'images/music/%Y/%m/%d/')
	slug = models.SlugField('url', unique=True)
	author = models.ForeignKey(User, verbose_name = 'Автор', related_name = 'author_track', on_delete = models.PROTECT)
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	likes = GenericRelation(Like)
	views = GenericRelation(Ip)

	def save(self):
		self.slug = slugify(self.track_title)
		super().save()

	class Meta:
		verbose_name = 'Трек'
		verbose_name_plural = 'Треки'

	def __str__(self):
		return self.slug
	
	@property
	def total_likes(self):
		return self.likes.count()

	@property
	def total_comments(self):
		return self.comment.count()

	@property
	def total_views(self):
		return self.views.count()

class Comment(models.Model):
	'''Модель комментария на сайте'''
	track = models.ForeignKey('Track', on_delete = models.CASCADE, verbose_name = 'Комментарий', related_name = 'comment')
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='track_comment_author')
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	comment_text = models.TextField('Текст комментария')
	likes = GenericRelation(Like)

	def __str__(self):
		'''При печатании объекта класса возвращает автора комментария'''
		return self.comment_text

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'

	@property
	def total_likes(self):
		return self.likes.count()
		
	@property
	def get_sub_comments(self):
		return self.sub_comment.all()

class SubComment(models.Model):
	'''Модель ответа к комментарию'''
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий', related_name='sub_comment')
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='music_sub_comment_author')
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	sub_comment_text = models.TextField('Текст комментария')

	class Meta:
		verbose_name = 'Подкомментарий'
		verbose_name_plural = 'Подкомментарии'
