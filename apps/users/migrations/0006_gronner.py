# Generated by Django 3.0.2 on 2020-01-25 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200125_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gronner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('extract', models.TextField()),
                ('dedication', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('full_name', models.CharField(max_length=70)),
                ('joined_at', models.DateField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
