# Generated by Django 3.0.2 on 2020-01-29 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20200127_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
