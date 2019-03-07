from django.contrib import admin

from news.models import NewsCategory, News, NewsAlbum

admin.site.register(NewsCategory)
admin.site.register(News)
admin.site.register(NewsAlbum)
