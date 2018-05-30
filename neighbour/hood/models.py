# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt

# Create your models here.


class Admin(models.Model):
    admin_name = models.CharField(max_length=50)


# class Profile(models.Model):
#     profilePic = models.ImageField(upload_to='profile/', null=True, blank=True)
#     bio = models.CharField(max_length=60, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.bio
#
#     def save_profile(self):
#         self.save()
#
#     def delete_profile(self):
#         self.delete()
#
#     @classmethod
#     def get_profile(cls):
#         profile = Profile.objects.all()
#         return profile
#
#     @classmethod
#     def find_profile(cls, search_term):
#         profile = cls.objects.filter(user__username__icontains=search_term)
#         return profile
#
#     @classmethod
#     def update_profile(cls, id, bio):
#         updated = Post.objects.filter(id=id).update(bio=bio)
#         return updated

class Neighbourhood(models.Model):
    neighbourhood_name = models.CharField(max_length=100)
    neighbourhood_icon = models.ImageField(upload_to='admin/', null=True, blank=True)
    neighbourhood_location = models.CharField(max_length=50)
    occuupants_count = models.CharField(max_length=500)
    admin = models.ForeignKey(Admin)

    def __str__(self):
        return self.neighbourhood_name

        def save_image(self):
            self.save()

            def delete_image(self):
                self.delete()

                def update_image(self):
                    self.update()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, blank=True)
    profilepic = models.ImageField(upload_to='profilepic/', null=True, blank=True)
    email = models.EmailField(max_length=100, null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, null=True, blank=True)
    bio = models.CharField(max_length=60, blank=True)

    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()
        return profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Business(models.Model):
    business_name = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    neighbourhood = models.ForeignKey(Neighbourhood)
    email = models.EmailField(max_length=80)

    def __str__(self):
        return self.location

    def save_location(self):
        self.save()

    def delete_location(self):
        self.delete()

    @classmethod
    def search_by_business_name(cls, search_term):
        images = cls.objects.filter(business_name__icontains=search_term)
        return images


class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    neighbourhood = models.ForeignKey(Neighbourhood)
    email = models.EmailField(max_length=80)
    business = models.ForeignKey(Business, null=True)

    def __str__(self):
        return self.user.username

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def update_image(self):
        self.update()

    @classmethod
    def search_by_category(cls, search_term):
        images = cls.objects.filter(category__name__icontains=search_term)
        return images

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Post(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    information = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def latest_showoffs(cls):
        today = dt.date.today()
        images = cls.objects.filter(pub_date__date=today)
        return images

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def update_image(self):
        self.update()

    @classmethod
    def get_images(cls):
        images = Post.objects.all()
        return images


class NeighbourhoodDetails(models.Model):
    detail = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    neighbourhood = models.ForeignKey(Neighbourhood, null=True)

    def __str__(self):
        return self.detail
