# Generated by Django 5.0.3 on 2024-03-19 10:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['-published_at']},
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_time'],
            },
        ),
    ]