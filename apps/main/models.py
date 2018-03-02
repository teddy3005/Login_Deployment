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
       


class travelManager(models.Manager):
    def travelval(self,postData):
        errors=[]
        if len(postData['destination'])==0:
            errors.append('Destination field cannot be blank')
        if len(postData['description'])==0:
            errors.append('Description field cannot be blank')
        if str(date.today())>str(postData['start']):
            errors.append('Input valid date')
        if str(date.today())>postData['end']:
            errors.append('Invalid date')
        if postData['start']> postData['end']:
            errors.append('Invalid date')
        if len(errors)==0:
            
            return (True)
        else:
            print 'unable to enter data'
            return (False, errors)
            
           

   
   


class User(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=UserManager()



class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start= models.DateField()
    end= models.DateField()
    creator= models.ForeignKey(User, related_name= "planner")
    join= models.ManyToManyField(User, related_name="joiner") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = travelManager()