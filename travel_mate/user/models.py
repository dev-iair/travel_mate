from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, UserManager

class User(AbstractBaseUser):
    name = models.CharField(primary_key=True, max_length=100)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'name'

    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'user'


class Content(models.Model):
    idx = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    fee = models.IntegerField()
    user_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'content'


class Payment(models.Model):
    idx = models.AutoField(primary_key=True)
    content_idx = models.ForeignKey('Content', db_column='content_idx', on_delete=models.CASCADE)
    name = models.ForeignKey('User', db_column='name', on_delete=models.CASCADE)
    pay = models.CharField(max_length=1, default='N')

    class Meta:
        managed = False
        db_table = 'payment'