# Generated by Django 5.0.3 on 2024-04-02 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_tag_alter_posts_options_hitcount_posttag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['-published_at']},
        ),
    ]
