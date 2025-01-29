from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class Location(models.Model):
    name = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)



