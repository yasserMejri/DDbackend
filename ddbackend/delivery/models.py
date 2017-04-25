# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class User_type(models.Model):
  type_name = models.CharField(max_length = 255)
  
  def __str__(self):
    return self.type_name

class DDUser(AbstractUser):
  first_name = models.CharField(max_length=255, blank=True)
  last_name = models.CharField(max_length=255, blank=True)
  phone = models.IntegerField(unique=True, validators=[RegexValidator(regex='^\d{14}$', message='Length has to be 10', code='Invalid number')], default=10000000000000)
  location = models.CharField(max_length=255, default="N/A")
  user_type = models.ForeignKey(User_type, default=0)
  
  def __str__(self):
    if self.first_name + self.last_name != '':
      return self.first_name + ' ' + self.last_name
    else:
      return self.username

class OrderStatus(models.Model):
  status_name = models.CharField(max_length = 255)
  
  def __str__(self):
    return self.status_name

class Order(models.Model):
  sender = models.ForeignKey(DDUser, related_name='send')
  receiver = models.ForeignKey(DDUser, related_name='receive')
  pick_up_location = models.CharField(max_length=255)
  drop_location = models.CharField(max_length=255)
  qrcode = models.FileField(upload_to='qrcode')
  status = models.ForeignKey(OrderStatus)

  def generate_qrcode(self):
    qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_L,
      box_size=12,
      border=0,
    )
    qr.add_data(self.sender.id)
    qr.add_data(self.pick_up_location)
    qr.add_data(self.drop_location)
    qr.add_data(self.receiver.id)
    qr.make(fit=True)

    img = qr.make_image()

    buffer = StringIO.StringIO()
    img.save(buffer)
    filename = 'order-%s.png' % (self.id)
    filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.len, None)
    self.qrcode.save(filename, filebuffer)

  def __str__(self):
    return self.sender.__str__() + ' to ' + self.receiver.__str__()

class Document(models.Model):
  name =models.CharField(max_length = 100)
  description = models.TextField()
  order = models.ForeignKey(Order)
  
  def __str__(self):
    return self.name

class OrderAction(models.Model):
  action_name = models.CharField(max_length = 255)
  
  def __str__(self):
    return self.action_name

class TrackStatus(models.Model):
  status_name = models.CharField(max_length = 255)
  
  def __str__(self):
    return self.status_name

class Track(models.Model):
  time = models.DateTimeField(auto_now=True)
  location1 = models.CharField(max_length=255)
  location2 = models.CharField(max_length=255)
  from_user = models.ForeignKey(DDUser, related_name='from_user')
  to_user = models.ForeignKey(DDUser, related_name='to_user')
  next_user = models.ForeignKey(DDUser, related_name="next_user")
  order = models.ForeignKey(Order)
  status = models.ForeignKey(TrackStatus)
  action = models.ForeignKey(OrderAction)
  
  def __str__(self):
    return self.time.strftime("%Y-%m-%d %H:%M:%S") + self.order.__str__()
