from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image, ExifTags
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
import os

class Dedication(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Gronner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    extract = models.TextField(default='', blank=True, null=True)
    dedication = models.ForeignKey(Dedication, default='Gronner', on_delete=models.SET_DEFAULT)
    points = models.IntegerField(default=0)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    country = CountryField(default='Argentina')

    def save(self, *args, **kwargs):
        super().save()
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

        img.save(self.image.path, file_format)


class Network(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class Social_media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    link = models.URLField(default='default.com')

    def __str__(self):
        str = self.network.name + ' (%s)'%(self.user.username) 
        return str
