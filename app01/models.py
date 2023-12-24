from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32)


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='static/form')

class Information(models.Model):
    id = models.AutoField(primary_key=True)
    realname = models.CharField(max_length=32)
    qianming = models.CharField(max_length=32)
    tel = models.CharField(max_length=32)
    age = models.CharField(max_length=32)
    gender = models.CharField(max_length=32)
    text = models.TextField()
    location = models.CharField(max_length=32)

class Comment(models.Model):
    nid=models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    time=models.CharField(max_length=32)
    com = models.TextField()

class History(models.Model):
    hid = models.IntegerField(max_length=32)
    username = models.CharField(max_length=32)

class ReComment(models.Model):
    nid=models.IntegerField(max_length=32)
    username = models.CharField(max_length=32)
    time=models.CharField(max_length=32)
    com = models.TextField()


