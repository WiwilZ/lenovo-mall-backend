from django.contrib.auth import get_user_model
from django.db import models

from goods.models import Goods


# 购物车
class ShoppingCart(models.Model):
    related_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='shopping_carts',
                                     related_query_name='shopping_cart')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
