from django.db import models

# Create your models here.
class Language(models.Model):
	lang = models.CharField(max_length=149, unique=True)
	slug = models.SlugField(max_length=149, default='lang')
	lang_code = models.SlugField(max_length=149, default='lang')

	def __str__(self):
		return self.lang