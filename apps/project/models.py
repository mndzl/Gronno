from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from PIL import Image, ExifTags
import os
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django_s3_storage.storage import S3Storage

storage = S3Storage(aws_s3_bucket_name=os.environ.get('AWS_STORAGE_BUCKET_NAME'))

class Category(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7)
    diminutive = models.CharField(max_length=10, default='Put here a diminutive name')

    def __str__(self):
        return self.name 


    def get_absolute_url(self):
        return reverse("category_explore", kwargs={"category": self.diminutive})

class Project(models.Model):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image1 = models.ImageField(storage=storage)
    image2 = models.ImageField(storage=storage)
    image3 = models.ImageField(storage=storage)

    def __str__(self):
        return self.title

    def get_date(self):
        time = timezone.now()

        segundos = int((time - self.date_posted).total_seconds())
        
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
                        return self.date_posted
                    else:
                        return f'hace {meses} meses'
                else:
                    return f'hace {dias} dias'
            else:
                return f'hace {horas} horas'
        else:
            return f'hace {minutos} minutos'


    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})

    """    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)      

        img = [Image.open(self.image1.path), Image.open(self.image2.path), Image.open(self.image3.path)]
        file_format = [img[0].format, img[1].format, img[2].format]
        
        for i in range(0,3):
            if file_format[i] == 'JPEG':
                exif = img[i]._getexif()
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
                        img[i] = img[i].transpose(rotate_values[orientation])

        for i in range(0,3):
            if img[i].height>1024 or img[i].width>768:
                output_size = (1024,768)
                img[i].thumbnail(output_size)

        img[0].save(self.image1.path, file_format[0])
        img[1].save(self.image2.path, file_format[1])
        img[2].save(self.image3.path, file_format[2]) """

    def suspend(self, reason):
        self.is_active = False
        self.author.gronner.points -= 500
        email = EmailMessage(
            'Proyecto eliminado',
            f"""Lo sentimos, tu proyecto {self.title} ha sido eliminado debido a que 
                la comunidad lo ha reportado por la siguiente razon: {reason}.
                
                Cualquier inconveniente puede responder este correo y lo ayudaremos a la brevedad.
                
                - Gronno Developers""",
            to=[self.author.email]
        )
        email.send()
        self.author.save()

class Medal(models.Model):
    medal_type = models.CharField(max_length=6)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.medal_type

class Award(models.Model):
    medal = models.ForeignKey(Medal, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s to %s"%(self.medal.medal_type, self.project.title)



class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    date_commented = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username + ' comments ' + self.project.title

    def get_date(self):
        time = timezone.now()

        segundos = int((time - self.date_commented).total_seconds())
        
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
                        return self.date_commented
                    else:
                        return f'hace {meses} meses'
                else:
                    return f'hace {dias} dias'
            else:
                return f'hace {horas} horas'
        else:
            return f'hace {minutos} minutos'

class Report(models.Model):
    reason = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
