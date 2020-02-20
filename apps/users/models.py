from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image, ExifTags
from apps.project.models import Category
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
import os
from django.utils import timezone
from apps.project.models import Project
from django.core.signals import request_finished
from django.db.models.signals import post_save

from django_s3_storage.storage import S3Storage

storage = S3Storage(aws_s3_bucket_name=os.environ.get('AWS_STORAGE_BUCKET_NAME'))

class Gronner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    extract = models.TextField(default='', blank=True, null=True)
    dedication = models.CharField(default='Gronner', max_length=40)
    points = models.IntegerField(default=0)
    image = models.ImageField(default='default.jpg', storage=storage)
    birth = models.DateField()
    categories_followed = models.ManyToManyField(Category, blank=True, null=True)
    country = CountryField(default='Argentina', blank=True, null=True)
    facebook = models.CharField(max_length=50,default='', blank=True)
    instagram = models.CharField(max_length=50, default='', blank=True)
    linkedin = models.CharField(max_length=50, default='', blank=True)
    twitter = models.CharField(max_length=50, default='', blank=True)
    shows_email = models.BooleanField(default=False)

    """ def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        file_format = img.format

        if file_format == 'JPEG':
            exif = img._getexif()

            # if image has exif data about orientation, let's rotate it
            orientation_key = 274 # cf ExifTags
            if exif and orientation_key in exif:
                orientation = exif[orientation_key]

                rotate_values = {
                    3: Image.ROTATE_180,
                    6: Image.ROTATE_270,
                    8: Image.ROTATE_90
                }

                if orientation in rotate_values:
                    img = img.transpose(rotate_values[orientation])
        
        if img.height>300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)

        img.save(self.image.path, file_format) """

    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.user.username})


    def notificate(self, other_user, reason, project, category):
        references = {
            'new_follow': {
                'icon': 'icon-user-check',
                'message': f'{other_user.get_full_name()} comenzó a seguirte',
                'color': '#19941d'
            },
            'new_following_project': {
                'icon': 'icon-plus',
                'message': f'{other_user.get_full_name()} subió un nuevo proyecto',
                'color': '#ba3e00'
            }
        }

        if category is not None:
            references.update({
                'new_category_project': {
                    'icon': f'icon-price-tag',
                    'message': f'Se ha subido un nuevo proyecto de {category.name}',
                    'color': category.color
                }
            })

        if project is not None:
            references.update({
                'new_Gold':{
                    'icon':'icon-medal',
                    'message': f'{other_user.get_full_name()} dió una medalla de oro a {project.title}',
                    'color': ' #D4AF37'
                }
            })

            references.update({
                'new_Silver': {
                    'icon':'icon-medal',
                    'message': f'{other_user.get_full_name()} dió una medalla de plata a {project.title}',
                    'color': '#C0C0C0'
                }
            })
            references.update({
                'new_Bronze': {
                    'icon': 'icon-medal',
                    'message': f'{other_user.get_full_name()} dió una medalla de bronce a {project.title}',
                    'color': '#CD7F32'
                }
            })
            references.update({
                'new_comment': {
                    'icon':'icon-bubble',
                    'message': f'{other_user.get_full_name()} comentó tu proyecto {project.title}',
                    'color': '#336ff2'
                }
            })

        if reason == 'new_follow':
            link = other_user.gronner.get_absolute_url()
        else:
            link = project.get_absolute_url()

        Notification.objects.create(
            user = self.user,
            message = references[reason]['message'],
            other_user = other_user,
            icon = references[reason]['icon'],
            link = link,
            color = references[reason]['color']
        )

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name = 'followers', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name = 'followings', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower} follows {self.following}'

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    other_user = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE, blank=True, null=True)
    icon = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=100, default='/')
    color = models.CharField(max_length=15, default='#000')
    seen = models.BooleanField(default=False)

    def notificate_followers(sender, **kwargs):
        if kwargs['created']:
            for follow in Follow.objects.filter(following=kwargs['instance'].author):
                follow.follower.gronner.notificate(other_user=kwargs['instance'].author, reason='new_following_project', project=kwargs['instance'], category=None)

            for category_follower in Gronner.objects.filter(categories_followed__in = [kwargs['instance'].category]):
                if category_follower.user not in Follow.objects.filter(following=kwargs['instance'].author):
                    category_follower.notificate(other_user=kwargs['instance'].author, reason='new_category_project', project=kwargs['instance'], category=kwargs['instance'].category)

    post_save.connect(notificate_followers, sender=Project)

    def get_date(self):
        time = timezone.now()

        segundos = int((time - self.date_created).total_seconds())
        
        if segundos<60:
            return f'hace {segundos} segundos'

        minutos = 0
        while segundos-60>=0:
            minutos += 1
            segundos -= 60
        if minutos>=60:
            horas = 0
            while minutos-60>=0:
                horas += 1
                minutos -= 60
            if horas>=24:
                dias = 0
                while horas-24>=0:
                    dias += 1
                    horas -= 24
                if dias>=31:
                    meses = 0
                    while dias-31>=0:
                        meses += 1
                        dias -= 31
                    if meses>=12:
                        return self.date_created
                    else:
                        return f'hace {meses} meses'
                else:
                    return f'hace {dias} dias'
            else:
                return f'hace {horas} horas'
        else:
            return f'hace {minutos} minutos'
