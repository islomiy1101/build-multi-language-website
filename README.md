### Django frameworkida web-saytni ko’p tilli qilish bo’yicha qo’llanma
___
#### 1.Yangi loyiha yaratamiz  
    django-admin startproject blog
#### 2. Loyihani ichida yangi app yaratamiz 
    python manage.py startapp news
#### 3. Appni loyihaga qo’shamiz
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #======= local app =======#
    'news',
]
```
#### 4. Loyihani ishga tushiramiz
     python manage.py runserver
![This is an image](https://miro.medium.com/max/854/1*n-yE8dKEeWUA7P0HvV0qeg.png)
#### 5. Loyiha uchun Article nomli model yaratamiz.
   Buning uchun _models.py_ fayliga kirib quyidagi kodni ko'chirib olamiz:
    
    from django.db import models
    from django.urls import reverse
    class Article(models.Model):
        title=models.CharField(max_length=255)
        slug=models.SlugField(unique=True)
        text=models.TextField()

        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse('')
#### 6. Article modelimizdagi maydonlarni bazada yaratish uchun
   quyidagi kommandalarni terminalga kiritib run qilamiz:

    python manage.py makemigrations
    python manage.py migrate
   admin panelga kirish uchun superuser yaratishimiz kerak uni quyidagicha yaratamiz:

    python manage.py createsuperuser

    Username (leave blank to use 'user'): admin
    Email address: islomiy1101@gmail.com
    Password: 123
    Password (again):123
    This password is too short. It must contain at least 8 characters.
    This password is too common.
    This password is entirely numeric.
    Bypass password validation and create user anyway? [y/N]: y
    Superuser created successfully.
#### 7. Modelimizni admin panelga qo'shamiz
   buning uchun __admin.py__ fayliga kirib quyidagi kodni ko'chiramiz:

    from django.contrib import admin
    from .models import Article
    @admin.register(Article)
    class ArticleAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug':('title',)}
#### 8. News app ichida urls.py faylini yaratamiz.
   va unga quyidagi kodni ko'chirib olamiz:
   
    from django.urls import path
    from .views import article_detail
    app_name='news'
    urlpatterns=[
        path('<slug:slug>/',article_detail,name='article_detail')
    ]

#### 9. _views.py_ faylida _article_detail_ nomli funksiya hosil qilamiz
    from django.shortcuts import render
    def article_detail(request,slug):
        context={
            'msg':'Hello World'
        }
    return render(request,'news/article_detail.html',context)

#### 10. Admin Panelga kirib yaratilgan tablega ma'lumot kiritamiz
![This is an image](https://github.com/islomiy1101/build-multi-language-website/blob/master/static/adminpanel.jpg?raw=true)

#### 11.Loyihaning urls.py faylini quyidagicha o’zgartiramiz
    from django.contrib import admin
    from django.urls import path,include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('',include('news.urls',namespace='news'))
    ]

#### 12. models.py fayliga o’zgartirish kiritamiz

    def get_absolute_url(self):
        return reverse('news:article_detail',kwargs={'slug':self.slug})

#### 13. Loyihada templates papkasini yaratamiz va uning ichida _news/article_detail.html_ fayl yaratamiz
    
    <div>
        <h2>Title: {{data.title}}</h2>
        <h4>Text: {{data.text}}</h4>
    </div>

#### 14. Ma'lumotlarni templatega chiqarish uchun views.py fayliga qo'shimchalar kiritamiz
    from django.shortcuts import render,get_object_or_404
    from .models import Article
    def article_detail(request,slug):
        data=get_object_or_404(Article,slug=slug)
        context={
            'data':data
        }
        return render(request,'news/article_detail.html',context)

#### 15. settings.py fayliga quyidagi kodlarni qo’shamiz
    from django.utils.translation import gettext_lazy as _

    LANGUAGES = [
        ('uz', _('Uzbek')),
        ('ru', _('Russian')),
        ('en', _('English')),
    ]
#### 16. Loyihaning urls.py fayliga o'zgartirish kiritamiz
    from django.conf.urls.i18n import i18n_patterns
    from django.contrib import admin
    from django.urls import path,include

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]+i18n_patterns(
        path('',include('news.urls',namespace='news'))
    )

#### 17. Article_detail.html fayliga quyidagi kodlar qatorini qo'shamiz
    
    {% load i18n %}

    <form action="{% url 'set_language' %}" method="post">{% csrf_token %}
        <input name="next" type="hidden" value="{{ redirect_to }}">
        <select name="language">
            {% get_current_language as LANGUAGE_CODE %}
            {% get_available_languages as LANGUAGES %}
            {% get_language_info_list for LANGUAGES as languages %}
            {% for language in languages %}
                <option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected{% endif %}>
                    {{ language.name_local }} ({{ language.code }})
                </option>
            {% endfor %}
        </select>
        <input type="submit" value="Go">
    </form>

#### 18. settings.py fayliga local middleware ni qo'shamiz
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
    ]

#### 19. Asosiy til uchun sayt urlidan _/uz/_ ni olib tashlash ya'ni default holatga uzbek tili deb tushunishi uchun
   buning uchun loyihaning urls.py fayliga kirib o'zgartirish qilamiz

    from django.conf.urls.i18n import i18n_patterns
    from django.contrib import admin
    from django.urls import path,include

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]+i18n_patterns(
        path('i18n/', include('django.conf.urls.i18n')),
        path('',include('news.urls',namespace='news'))
        prefix_default_language=False

![This is an image](https://github.com/islomiy1101/build-multi-language-website/blob/master/static/pro.jpg?raw=true)

#### 20. Loyihamizda foydalanish uchun django modeltranslation packagini o'rnatib olamiz
buning uchun terminalda quyidagi kommandani beramiz:

    pip install django-modeltranslation

#### 21. modelni settings.py fayliga qo'shamiz
    INSTALLED_APPS = [
    'modeltranslation',#eng boshiga qo’shiladi
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news'
]

    MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
    MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'en'

#### 22. Modelimizni Translationga bog'laymiz.
 buning uchun news app ichida translation.py faylini yaratamiz va unga quyidagi kodlar ketma-ketligini kiritamiz:

    from modeltranslation.translator import register, TranslationOptions
    from news.models import Article

    @register(Article)
    class ArticleTranslationOptions(TranslationOptions):
        fields = ('title', 'text',)
shundan so'ng, 

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

admin panelga kirganimizda quyigicha ko'rinish hosil bo'lgan bo'ladi

![This is an image](https://github.com/islomiy1101/build-multi-language-website/blob/master/static/photo_2022-06-05_22-10-27.jpg?raw=true)

#### 23. Endi esa Admin Panelga integratsiyalaymiz
buning uchun admin.py fayliga quyidagicha o'zgartirish kiritamiz:
    
    from modeltranslation.admin import TranslationAdmin
    from django.contrib import admin
    from .models import Article

    @admin.register(Article)
    class ArticleAdmin(TranslationAdmin):
        prepopulated_fields = {'slug':('title',)}

#### 24. Rasmdan ko'rishiz mumkin endi saytimiz 3 xil tilda ishlamoqda
![This is an image](https://github.com/islomiy1101/build-multi-language-website/blob/master/static/11.jpg?raw=true)


#### 25.Bizda mana bazadan kelayotgan ma’lumotlar o’zgarmoqda endi saytdagi menyular yoki footer qismidagi textlarni o’zgartirish ni ko'rib chiqamiz.
Buning uchun article_detail.html fayliga qo’shimcha kiritamiz.

    <div>
        <h2>Title: {% trans 'Template Title' %}</h2>
        <h2>Text: {% trans 'Template Text' %}</h2>
    </div>

#### 26.settings.py fayliga quyidagi kodni yozamiz va terminala quyidagi komandani beramiz
    #settings.py fayliga qo’shamiz

    LOCALE_PATHS = [
        BASE_DIR/'locale']

    #terminalda da quyidagi command ni beramiz
        py manage.py makemessages -l uz

#### 27. Shundan so'ng bizni loyihamizda locale papkasi yaratiladi va uni ichidagi LC_MESSAGES papkasidagi Django.po faylini ichiga kirib quyidagicha o'zgartirish kiritamiz
    #: .\news\templates\news\article_detail.html:22
    msgid "Template Title"
    msgstr "Shablon Sarlavhasi"

    #: .\news\templates\news\article_detail.html:23
    msgid "Template Text"
    msgstr "Shablon matni"

#### 28. O'zgartirishlarni saqlagandan so’ng quyidagi kommandani terminalga kiritamiz va run qilamiz
    python manage.py compilemessages

#### 29.Endi esa rus tiliga o’girish uchun 
    #terminalda da quyidagi command ni beramiz
    py manage.py makemessages -l ru

 Qayta django.po faylini ichiga kirib quyidagicha o'zgartirish kiritamiz

    #: .\news\templates\news\article_detail.html:22
    msgid "Template Title"
    msgstr "Заголовок в шаблон"

    #: .\news\templates\news\article_detail.html:23
    msgid "Template Text"
    msgstr "Текст в шаблон"

O'zgartirishlarni saqlagandan so’ng quyidagi kommandani terminalga kiritamiz va run qilamiz

    python manage.py compilemessages

#### 30. Admin Paneldagi tablitsalarga tegishli bo'lgan maydon nomlarini tilini o’zgartirish.
buning uchun, models.py fayliga qo’shimcha kiritamiz

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

#### 31. Endi esa yana quyidagi kommandani terminalda beramiz
    #terminalda da quyidagi command ni beramiz
    py manage.py makemessages -l uz
shundan so'ng django.py fayliga kirib o'zgaritirish qilamiz

    #: .\news\models.py:5
    msgid "title"
    msgstr "Sarlavha"

    #: .\news\models.py:6
    msgid "slug"
    msgstr "Yopishqoq"

    #: .\news\models.py:7
    msgid "text"
    msgstr "Matn"
O'zgarishlarni saqlagandan so'ng,terminalda quyidagi kommandani beramiz:

    python manage.py compilemessages

#### 32. JavaScript orqali templatega chiqarilgan ma'lumotlarni tilini o'zgartirishni ko'rib chiqamiz
Buning uchun loyihamiz ichida static nomli papka yaratamiz va uning ichiga __app.js__ nomi bilan javascript faylini yaratib uning ichiga quyidagi kodni yozamiz:

    const msg='Xush kelibsiz,Mehmon'
    document.body.innerHTML+=`<hr><h1>${msg}</h1>`

#### 33. Loyihaning urls.py fayliga qoshimcha kiritamiz
    from django.conf.urls.i18n import i18n_patterns
    from django.contrib import admin
    from django.urls import path,include
    from django.views.i18n import JavaScriptCatalog

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]+i18n_patterns(
        path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
        path('i18n/', include('django.conf.urls.i18n')),
        path('',include('news.urls',namespace='news')),
        prefix_default_language=False
    )
shundan so'ng,article_detail.html fayliga quyidai kodni qo'shib qo'yamiz

    <script src="{% url 'javascript-catalog' %}"></script>

#### 34. Endi js faylidagi ma'lumotni tilini o'zgartirish uchun terminalga quyidagi kommandani beramiz
    py manage.py makemessages -l uz -d djangojs
shundan so'ng djangojs.po fayli yaratiladi va uning ichida o'zgartirishlarni amalga oshirgandan so'ng qayta compilatsiya qilamiz

    py manage.py compilemessages

Vanihoyat saytimiz tayyor bo'ldi endi saytni tilini o'zgartirganimizda nafaqat bazadan kelayotgan ma'lumot qo'yingi barcha static holatda yozilgan matnlar xam tarjima bo'ladi.E'tiboriz uchun raxmat 😊!!!
