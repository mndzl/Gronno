# Generated by Django 3.0.2 on 2020-02-04 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20200204_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image1',
            field=models.ImageField(upload_to='project_pics'),
        ),
        migrations.AlterField(
            model_name='project',
            name='image2',
            field=models.ImageField(upload_to='project_pics'),
        ),
        migrations.AlterField(
            model_name='project',
            name='image3',
            field=models.ImageField(upload_to='project_pics'),
        ),
    ]