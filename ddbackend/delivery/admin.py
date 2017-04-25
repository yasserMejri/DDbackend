# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from delivery import models

admin.site.register(models.User_type)
admin.site.register(models.DDUser)
admin.site.register(models.Order)
admin.site.register(models.OrderStatus)
admin.site.register(models.Track)
admin.site.register(models.TrackStatus)

# Register your models here.
