# Generated by Django 3.0.2 on 2020-02-02 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0010_reportcomment_reportproject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='reportproject',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
        migrations.DeleteModel(
            name='ReportComment',
        ),
        migrations.DeleteModel(
            name='ReportProject',
        ),
        migrations.AddField(
            model_name='report',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
