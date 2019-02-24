from django.contrib import admin

from goods.models import GoodsCategory, Goods, GoodsAlbum

admin.site.register(GoodsCategory)
admin.site.register(Goods)
admin.site.register(GoodsAlbum)
