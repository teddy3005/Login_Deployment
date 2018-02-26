from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request,'main/index.html')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        if request.POST.get('email')=='' or request.POST.get('password')=='':
            messages.error(request, 'Field cannot be blank')
            return redirect('/')
        #check if the email is in db
        user=User.objects.filter(email=request.POST.get('email')).first()
        #if it is veritfy the pw
        if user and bcrypt.checkpw(request.POST.get('password').encode(),user.password.encode()):
            request.session['user']=user
            return redirect('/show')
        else:
            messages.error(request,'Email and password provided did not match')
            return redirect ('/')

def createUser(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        check= User.objects.validateUser(request.POST)
        #create error message improt messages!
        if check[0]==False:
            for error in check[1]:
                messages.error(request, error)
            return redirect('/')
        else:
            #create the user
            user=User.objects.filter(email=request.POST.get('email')).first()
            #add the user to session
            hashed_pw=bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
            user=User.objects.create(
                name = request.POST.get('name'),
                email = request.POST.get('email'),
                password = hashed_pw
                )
            request.session['user']=user
            return redirect('/show')
    
def view_result(request):
    context = {
        'current_user':request.session['user'],
       }
   
    return render(request, 'main/show.html', context)