# Generated by Django 3.0.3 on 2020-02-18 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.URLField(default=2),
            preserve_default=False,
        ),
    ]
