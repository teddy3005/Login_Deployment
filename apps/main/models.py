from __future__ import unicode_literals
import re
from datetime import date, datetime
from django.db import models 
import bcrypt

class UserManager(models.Manager):
    def validateUser(self,post):
        is_valid=True
        errors=[]
        if len(post.get('name'))==0:
            is_valid=False
            errors.append('Name field cannot be blank!')
        if len(post.get('name'))<3:
            is_valid=False
            errors.append('name must 3 characters or more')
        if not re.search(r'\w+\@\w+\.\w+',post.get('email')):
            is_valid=False
            errors.append('Please provide a valid email address')
        if len(User.objects.filter(email=post['email'])) > 0:
            is_valid=False
            errors.append('Email Already in Use!')
        if len(post.get('password')) == 0:
            is_valid=False
            errors.append('Password cannot be blank')
        if len(post.get('password')) < 8:
            is_valid=False
            errors.append('Password must be 8 characters or longer')
        if post.get('password') != post.get('password_confirmation'):
            is_valid=False
            errors.append('Password provided does not match!')
        return (is_valid, errors)
       


               
class AppointmentManager(models.Manager):
    def appointment_val(self,postData):
        errors={}
        if postData['task']==0:
            errors.append('Field cannot be empty')
        if postData['date']==0:
            errors.append('Please select a valid date')
        return errors
   


class User(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=UserManager()



class Appointment(models.Model):
    task = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    date = models.DateField(blank=False)
    user = models.ForeignKey(User, related_name="appointment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()

    def is_today(self):
        return {'date':datetime.now()}