from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from goods.models import Goods
from receiving_address.models import ReceivingAddress


# 订单
class Order(models.Model):
    ORDER_STATUS = (
        ('TO_BE_PAID', '待付款'),
        ("TO_BE_SHIPPED", '待发货'),
        ("TO_BE_RECEIVED", "待收货"),
        ('COMPLETED', '已完成'),
        ("CANCELLED", "已取消")
    )

    related_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders',
                                     related_query_name='order')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='goods', related_query_name='goods')
    count = models.PositiveIntegerField(default=0)
    receiving_address = models.ForeignKey(ReceivingAddress, on_delete=models.CASCADE, verbose_name='收货信息')
    status = models.CharField(default='TO_BE_PAID', choices=ORDER_STATUS, max_length=128)
    time_created = models.DateTimeField(default=timezone.now)
    time_paid = models.DateTimeField(blank=True, null=True)
    time_shipped = models.DateTimeField(blank=True, null=True)
    time_received = models.DateTimeField(blank=True, null=True)
