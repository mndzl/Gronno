from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Gronner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    extract = models.TextField(default='', blank=True, null=True)
    dedication = models.CharField(max_length=20)
    points = models.IntegerField(default=0)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

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


