# Generated by Django 3.0.2 on 2020-02-04 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20200202_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_commented',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]