from django.db import models
from django.contrib.auth.models import User

class Social_Network(models.Model):
    name = models.CharField(max_length=20)
    link = models.URLField(verify_exists = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE)