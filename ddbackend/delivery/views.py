# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from delivery import models

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json

loggeduser = None

class Auth(View):
  action = ''

  def authenticate_via_email(self, email, password):
    """
        Authenticate user using email.
        Returns user object if authenticated else None
    """
    if email:
      try:
        user = models.DDUser.objects.get(email__iexact=email)
        if user.check_password(password):
          return user
      except :
        pass
    return None  
  
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super(Auth, self).dispatch(request, *args, **kwargs) 
  
  def get(self, request, *args, **kwargs):
    return HttpResponse("Only Post requests are allowed")
  
  def post(self, request, *args, **kwargs):
    global loggeduser
    param = json.loads(request.body)
    
    if param['action'] == 'login':
      user = self.authenticate_via_email(email=param['email'], password=param['password'])
      if user is not None:
        login(request, user)
        loggeduser = user
        return HttpResponse(json.dumps({
          'status': 'success', 
          'user_id': user.id, 
          'user_type': user.user_type.type_name
        }))
      else :
        return HttpResponse(json.dumps({
          'status': 'fail', 
          'message': 'Login Failed'
        }))
    elif param['action']== 'logout':
      logout(request)
      return HttpResponse(json.dumps({
        'status': 'success', 
      }))
    elif param['action'] == 'register':
      user = models.DDUser(
        username = param['username'], 
        phone = param['phone'], 
        location = param['location'],
        first_name = param['first_name'],
        last_name = param['last_name'], 
        email = param['email']
      )
      user.save()
      user.set_password(param['password'])
      return HttpResponse(json.dumps({
        'status': 'success', 
        'user_id': user.id, 
        'user_email': user.email, 
        'user_location': user.location
      }))
    elif param['action'] == 'getprofile':
      user = loggeduser
      try:
        return HttpResponse(json.dumps({
          'status': 'success', 
          'email': user.email, 
          'username': user.username, 
          'phone': user.phone, 
          'location': user.location
        }))
      except:
        return HttpResponse(json.dumps({
          'status': 'error', 
          'user': user
        }))
    return HttpResponse(json.dumps({
      'status': 'empty', 
      'message': 'Invalid Auth Request', 
      'request': param
    }))

  
  
class Order(View):
  def get(request):
    return HttpResponse("Only post requests allowed")
  def post(requests):
    return HttpResponse("To be implemented")