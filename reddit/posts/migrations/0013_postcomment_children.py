# Generated by Django 3.0.7 on 2020-07-04 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20200704_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='children',
            field=models.ManyToManyField(to='posts.PostComment'),
        ),
    ]
