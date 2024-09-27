from django.db import models

from order.models import Order
from profiles.models import UserProfile


class Payment(models.Model):
    number = models.CharField(max_length=16)
    name = models.CharField(max_length=20)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    code = models.CharField(max_length=3)
    payment_user_profile = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    payment_num_orders = models.OneToOneField(Order, on_delete=models.DO_NOTHING)
