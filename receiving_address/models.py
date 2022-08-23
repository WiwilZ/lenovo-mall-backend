from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# 收货地址
class ReceivingAddress(models.Model):
    related_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='receiving_addresses',
                                     related_query_name='receiving_address')
    consignee = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    is_default = models.BooleanField(default=False)
