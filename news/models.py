from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
class Article(models.Model):
    title=models.CharField(verbose_name=_('title'),max_length=255)
    slug=models.SlugField(verbose_name=_('slug'),unique=True)
    text=models.TextField(verbose_name=_('text'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:article_detail',kwargs={'slug':self.slug})