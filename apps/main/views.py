from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'main/index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validation(request.POST)
        if 'user' in errors:
            request.session['currentuser']=errors['user']
            
            return redirect('/dashboard')
        else:
            for register,error in errors.iteritems():
                messages.error(request, error, extra_tags=register)
            return redirect('/index2')
    else:
        return redirect('/index2')

def new(request):
    return render(request, 'main/index2.html')

def login(request):
    if request.method == 'POST':
        checklogin = User.objects.loginvalidation(request.POST)
        if "user" in checklogin:
            request.session['currentuser']= checklogin["user"]
            request.session["idk"]= "logged in"
            return redirect('/dashboard')
        else:
            for tag, error in checklogin.iteritems():
                messages.error(request, error, extra_tags=tag)
                return redirect('/main')
    else:
        return redirect('/main')
    
    
    
def success(request):
    if 'currentuser' in request.session:
        showuser= request.session['currentuser']
        context={
            'currentuser':showuser,
        }
        return render(request, 'main/success.html',context)
    else:
        return redirect ('/main')




def logout(request):
    request.session.clear()
    return redirect ('/')


  