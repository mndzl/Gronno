# Generated by Django 3.0.2 on 2020-01-23 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200123_1645'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Social_media',
            new_name='Network',
        ),
    ]