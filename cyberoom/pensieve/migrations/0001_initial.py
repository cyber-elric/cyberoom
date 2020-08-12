# Generated by Django 3.0.6 on 2020-08-12 10:25

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pensieve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=66, unique=True)),
                ('content', tinymce.models.HTMLField(blank=True)),
                ('upDate', models.DateTimeField(auto_now=True)),
                ('up', models.CharField(max_length=60)),
            ],
            options={
                'ordering': ['-upDate'],
            },
        ),
    ]
