# Generated by Django 3.0.6 on 2020-08-04 02:36

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('pensieve', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pensieve',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
