from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from slugify import slugify

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	image = models.ImageField('Фото', upload_to='images/private_office/%Y/%m/%d/', blank=True)
	slug = models.SlugField('url', unique=True)

	class Meta:
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профили'

	def __str__(self):
		return self.user.username

	@property
	def total_likes(self):
		return self.user.like.count()

	@property
	def total_comments(self):
		return self.user.track_comment_author.count() + self.user.article_comment_author.count() + self.user.art_comment_author.count()

	@property
	def total_posts(self):
		return self.user.article.count() + self.user.art.count() + self.user.author_track.count()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, slug=slugify(instance.username))

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class History(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
	model = models.CharField('Название модели', max_length=255)
	record_id = models.IntegerField(verbose_name='ID записи', null=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'История'
		verbose_name_plural = 'История'

	def __str__(self):
		return self.model