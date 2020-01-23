from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Network(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class Social_media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    link = models.URLField(default='default.com')
