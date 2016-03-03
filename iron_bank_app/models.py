from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    customer = models.ForeignKey(User)
    description = models.TextField(blank=True)
    balance = models.FloatField(default=0)
    initial_balance = models.FloatField(default=0)
    account_created = models.DateTimeField(auto_now_add=True)

