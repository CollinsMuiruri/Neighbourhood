# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Admin(models.Model):
    admin_name = models.CharField(max_length=50)


class Neighbourhood(models.Model):
    neighbourhood_name = models.CharField(max_length=100)
    neighbourhood_location = models.CharField(max_length=50)
    occuupants_count = models.CharField(max_length=500)
    admin = models.ForeignKey(Admin)


class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    # user_id = models.AutoField(primary_key=True)
    neighbourhood = models.ForeignKey(Neighbourhood)
    email = models.EmailField(max_length=80)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Business(models.Model):
    business_name = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    neighbourhood = models.ForeignKey(Neighbourhood)
    email = models.EmailField(max_length=80)
