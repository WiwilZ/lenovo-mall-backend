from uuid import uuid4

from django.db import models
from django.utils import timezone


# 商品分类
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


# 品牌
class Brand(models.Model):
    name = models.CharField(max_length=128, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands', related_query_name='brand')


# 商品
class Goods(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='goods', related_query_name='goods')
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=512, blank=True)
    sales = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    color = models.CharField(max_length=128, unique=True, blank=True)
    cpu = models.CharField(max_length=128, unique=True, blank=True)
    memory = models.CharField(max_length=128, unique=True, blank=True)
    hard_disk = models.CharField(max_length=128, unique=True, blank=True)
    graphics_card = models.CharField(max_length=128, unique=True, blank=True)
    time_created = models.DateTimeField(default=timezone.now)


def path_and_rename(instance, filename):
    return f'goods/{uuid4().hex}.{filename.split(".")[-1]}'


# 图片
class Picture(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='pictures', related_query_name='picture')
    picture = models.ImageField(upload_to=path_and_rename)
