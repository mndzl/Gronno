from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField()

    def __str__(self):
        return self.name + '(%s)' %self.color

class Project(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Medal(models.Model):
    name = models.CharField(max_length=6)
    project = models.ManyToManyField(Project)

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

