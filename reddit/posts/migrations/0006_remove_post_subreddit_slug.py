# Generated by Django 3.0.7 on 2020-06-25 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20200625_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='subreddit_slug',
        ),
    ]
