from django.contrib import admin

from .models import Category, Goods, Brand, Picture

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Goods)
admin.site.register(Picture)
