from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7)
    diminutive = models.CharField(max_length=10, default='Put here a diminutive name')

    def __str__(self):
        return self.name + ' (%s, %s)' %(self.color, self.diminutive)

class Project(models.Model):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_date(self):
        time = datetime.now()

        if self.date_posted.hour == time.hour:
            return "hace " + str(time.minute - self.date_posted.minute) + " minuto/s"
        else:
            if self.date_posted.day == time.day:
                return "hace " + str(time.hour - self.date_posted.hour) + " hora/s"
            else:
                if self.date_posted.month == time.month:
                    return "hace " + str(time.day - self.date_posted.day) + " dia/s"
                else:
                    if self.date_posted.year == time.year:
                        return "hace " + str(time.month - self.date_posted.month) + " mes/es"
        return self.date_posted

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})


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

    def get_date(self):
        time = datetime.now()

        if self.date_commented.hour == time.hour:
            return "hace " + str(time.minute - self.date_commented.minute) + " minutos"
        else:
            if self.date_commented.day == time.day:
                return "hace " + str(time.hour - self.date_commented.hour) + " horas"
            else:
                if self.date_commented.month == time.month:
                    return "hace " + str(time.day - self.date_commented.day) + " dias"
                else:
                    if self.date_commented.year == time.year:
                        return "hace " + str(time.month - self.date_commented.month) + " meses"
        return self.date_commented