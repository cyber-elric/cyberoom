# coding = utf8

from django.db import models


# Create your models here.
class TheKey(models.Model):
    owner = models.CharField(unique=True, max_length=60)
    shape = models.CharField(unique=True, max_length=36)

