from __future__ import unicode_literals
import re
import datetime
from django.db import models

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
        if post.get('password') != post.get('password_confirmation'):
            is_valid=False
            errors.append('Password provided does not match!')
        return (is_valid, errors)
       



   
   


class User(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    # date_hired=models.DateField()
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=UserManager()



