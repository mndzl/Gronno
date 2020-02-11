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


from django_s3_storage.storage import S3Storage

storage = S3Storage(aws_s3_bucket_name=os.environ.get('AWS_STORAGE_BUCKET_NAME'))

class Gronner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    extract = models.TextField(default='', blank=True, null=True)
    dedication = models.CharField(default='Gronner', max_length=40)
    points = models.IntegerField(default=0)
    image = models.ImageField(default='https://gronno-media.s3.amazonaws.com/default.jpg', storage=storage)
    birth = models.DateField()
    categories_followed = models.ManyToManyField(Category)
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

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name = 'followers', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name = 'followings', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower} follows {self.following}'