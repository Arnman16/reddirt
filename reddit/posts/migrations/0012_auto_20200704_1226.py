# Generated by Django 3.0.7 on 2020-07-04 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_postcomment_parent_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcomment',
            old_name='parent_comment',
            new_name='parent',
        ),
    ]