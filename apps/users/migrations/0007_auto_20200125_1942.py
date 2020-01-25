# Generated by Django 3.0.2 on 2020-01-25 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_gronner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gronner',
            name='joined_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='social_media',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Gronner'),
        ),
    ]
