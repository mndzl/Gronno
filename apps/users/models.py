from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser

class Gronner(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    extract = models.TextField()
    dedication = models.CharField(max_length=20)
    email = models.EmailField()
    full_name = models.CharField(max_length=70)
    joined_at = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'username']

    def get_full_name(self):
        return self.full_name

class Network(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class Social_media(models.Model):
    user = models.ForeignKey(Gronner, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    link = models.URLField(default='default.com')

    def __str__(self):
        str = self.network.name + ' (%s)'%(self.user.username) 
        return str


