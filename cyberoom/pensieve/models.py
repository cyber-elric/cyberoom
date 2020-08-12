# coding = utf-8

from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class Pensieve(models.Model):
    title = models.CharField(unique=True, max_length=66)
    content = HTMLField(blank=True)
    upDate = models.DateTimeField(auto_now=True)
    up = models.CharField(max_length=60)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pensieve:list')

    class Meta:
        ordering = ['-upDate']
