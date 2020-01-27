from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7)
    diminutive = models.CharField(max_length=10, default='Put here a diminutive name')

    def __str__(self):
        return self.name + ' (%s, %s)' %(self.color, self.diminutive)

class Project(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

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
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username + ' comments ' + self.project.title
