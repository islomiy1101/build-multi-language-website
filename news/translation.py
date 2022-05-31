from modeltranslation.translator import register, TranslationOptions
from news.models import Article

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)