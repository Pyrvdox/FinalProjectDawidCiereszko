from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    department = models.CharField(max_length=128)
    code = models.CharField(max_length=8)


class Tech(models.Model):
    name = models.CharField(max_length=128)
    desc = models.TextField()
    icon = models.ImageField(upload_to='images/')
    tickets = models.ManyToManyField('Techticket', related_name='items')

    def __str__(self):
        return f"{self.name}"


class App(models.Model):
    name = models.CharField(max_length=256)
    desc = models.TextField()
    icon = models.ImageField(upload_to='images/')
    tickets = models.ManyToManyField('Appticket', related_name='apps')

    def __str__(self):
        return f"{self.name}"


class Techticket(models.Model):
    item = models.ForeignKey('Tech',on_delete=models.DO_NOTHING)
    author = models.ForeignKey('CustomUser', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    feedback = models.TextField()
    status = models.CharField(max_length=32)


class Appticket(models.Model):
    item = models.ForeignKey('App',on_delete=models.DO_NOTHING)
    author = models.ForeignKey('CustomUser', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    feedback = models.TextField()
    status = models.CharField(max_length=32)
