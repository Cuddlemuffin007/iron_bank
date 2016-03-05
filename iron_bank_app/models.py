from django.contrib.auth.models import User
from django.db import models

CHOICES = [('d', 'deposit'), ('w', 'withdrawal'), ('t', 'transfer')]


class Account(models.Model):
    customer = models.ForeignKey(User)
    nickname = models.CharField(max_length=20)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    initial_balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    account_created = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=20, blank=True)
    transaction_type = models.CharField(max_length=10, choices=CHOICES)
    destination_account_id = models.IntegerField(null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)




