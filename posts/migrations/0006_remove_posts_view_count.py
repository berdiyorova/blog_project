# Generated by Django 5.0.3 on 2024-04-01 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_posts_recommended'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='view_count',
        ),
    ]