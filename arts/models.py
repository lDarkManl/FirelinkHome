from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import Like
from ip.models import Ip
from services.services import slugify

class Art(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='art')
	title = models.CharField('Название', unique=True, max_length=255)
	title_seo = models.CharField('Название в поиске', unique=True, max_length=255, blank=True)
	slug = models.SlugField('url', unique=True)
	image = models.ImageField('Арт', upload_to = 'images/arts/%Y/%m/%d/')
	content = RichTextUploadingField('Информация об арте', blank=True)
	image_alt = models.TextField('Атрибут alt', default='god of war')
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	tags = models.ManyToManyField('Tag', verbose_name='Тег', related_name='tags')
	likes = GenericRelation(Like)
	views = GenericRelation(Ip)

	def save(self):
		self.slug = slugify(self.title)
		super().save()

	class Meta:
		verbose_name = 'Арт'
		verbose_name_plural = 'Арты'

	def __str__(self):
		return self.author.username

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
	art = models.ForeignKey('Art', on_delete = models.CASCADE, verbose_name = 'Комментарий', related_name = 'comment')
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='art_comment_author')
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	comment_text = models.TextField('Текст комментария')
	likes = GenericRelation(Like)

	def __str__(self):
		'''При печатании объекта класса возвращает автора комментария'''
		return self.author.username

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
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='art_sub_comment_author')
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	sub_comment_text = models.TextField('Текст комментария')

	class Meta:
		verbose_name = 'Подкомментарий'
		verbose_name_plural = 'Подкомментарии'

class Tag(models.Model):
	name = models.CharField('Имя тега', max_length=50)
	slug = models.SlugField('url тега', max_length=50)

	class Meta:
		verbose_name = 'Тег'
		verbose_name_plural = 'Теги'
		
	def __str__(self):
		return self.slug