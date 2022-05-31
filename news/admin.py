from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    prepopulated_fields = {'slug':('title',)}
