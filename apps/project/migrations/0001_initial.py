# Generated by Django 3.0.3 on 2020-02-11 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_s3_storage.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('color', models.CharField(max_length=7)),
                ('diminutive', models.CharField(default='Put here a diminutive name', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Medal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medal_type', models.CharField(max_length=6)),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, unique=True)),
                ('description', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('points', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('image1', models.ImageField(storage=django_s3_storage.storage.S3Storage(aws_s3_bucket_name='gronno-media'), upload_to='')),
                ('image2', models.ImageField(storage=django_s3_storage.storage.S3Storage(aws_s3_bucket_name='gronno-media'), upload_to='')),
                ('image3', models.ImageField(storage=django_s3_storage.storage.S3Storage(aws_s3_bucket_name='gronno-media'), upload_to='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=50)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date_commented', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Medal')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
