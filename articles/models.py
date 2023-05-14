from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import Like
from ip.models import Ip

class Article(models.Model):
	'''Модель статьи на сайте'''
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='article')
	article_title = models.CharField('Название статьи', max_length = 100)
	article_title_seo = models.CharField('Название статьи в поиске', max_length = 100)
	article_content = RichTextUploadingField('Содержание статьи')
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	update_date = models.DateTimeField('Дата обновления', auto_now = True)
	article_image = models.ImageField('Фото', upload_to = 'images/articles/%Y/%m/%d/')
	article_image_alt = models.TextField('Атрибут alt')
	is_published = models.BooleanField('Статус публикации', default = True)
	article_game = models.ForeignKey('Game', on_delete = models.PROTECT, verbose_name = 'Игра', related_name = 'game')
	article_category = models.ForeignKey('Category', on_delete = models.PROTECT, verbose_name = 'Категория', related_name = 'category')
	article_video = models.URLField('Ссылка на видео', blank = True)
	likes = GenericRelation(Like)
	views = GenericRelation(Ip)

	def __str__(self):
		'''Возвращает название статьи при печатании объекта класса'''
		return self.article_title
	
	@property
	def total_likes(self):
		return self.likes.count()

	@property
	def total_comments(self):
		return self.comment.count()
			
	class Meta:
		verbose_name = 'Статья'
		verbose_name_plural = 'Статьи'
		ordering = ['-pub_date']

	@property
	def total_views(self):
		return self.views.count()
	

class Game(models.Model):
	'''Модель игры для статьи'''
	game_title = models.CharField('Название игры', max_length = 100)
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	update_date = models.DateTimeField('Дата обновления', auto_now = True)
	game_title_meta = models.CharField('Название игры на мета уровне', max_length = 100)

	def __str__(self):
		'''Возвращает название игры при печатании объекта класса'''
		return self.game_title

	class Meta:
		verbose_name = 'Игра'
		verbose_name_plural = 'Игры'


class Category(models.Model):
	'''Модель категории статей'''
	category_title = models.CharField('Название категории', max_length = 100)
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	update_date = models.DateTimeField('Дата обновления', auto_now = True)
	category_title_meta = models.CharField('Название категории на мета уровне', max_length = 100)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		'''Возвращает категорию при печатании объекта класса'''
		return self.category_title


class Comment(models.Model):
	'''Модель комментария на сайте'''
	article = models.ForeignKey('Article', on_delete = models.PROTECT, verbose_name = 'Статья', related_name = 'comment')
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='article_comment_author')
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
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='article_sub_comment_author')
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	sub_comment_text = models.TextField('Текст комментария')

	class Meta:
		verbose_name = 'Подкомментарий'
		verbose_name_plural = 'Подкомментарии'

		