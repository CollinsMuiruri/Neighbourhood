# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from hood.models import UserProfileModel


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_name', 'neighbourhood', 'email']

# Register your models here.


admin.site.register(UserProfileModel, UserProfileAdmin)
