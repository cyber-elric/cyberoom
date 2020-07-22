# coding = utf-8

from django.db import models
from django.urls import reverse


class Pensieve(models.Model):
    title = models.CharField(unique=True, max_length=66)
    content = models.TextField()
    upDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pensieve:list')

    class Meta:
        ordering = ['-upDate']
