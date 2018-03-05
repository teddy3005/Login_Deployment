from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import json
import operator
from datetime import datetime 


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
    

def dashboard(request):
    if 'user' in request.session:
        today=datetime.now().strftime("%Y-%m-%d")
        user= User.objects.get(id=request.session['user'].id)
        context={
            'user':request.session['user'],
            'today':Appointment.objects.order_by('time').filter(date=today, user=user),
            'later':Appointment.objects.order_by('time').filter(user=user).exclude(date=today)
        }
        return render(request, 'main/show.html',context, today)
    else:
        return redirect ('/')

def edit(request):
    if 'user' not in request.session:
        return redirect('/')
    else:
        user=User.objects.get(id=request.session['user'])
    return render(request, 'main/create.html')

def update(request,id):
    errors=Appointment.objects.appointment_val(request.POST)
    if "exist" in errors:
        for tag, error in errors.iteritems():
            messages.errors(request, error, extra_tags=tag)
        return redirect("main/show")
    else:
        app =Appointment.objects.get(id=id)
        app.task=request.POST['task']
        app.date=request.POST['date']
        app.time=request.POST['time']
        app.status=request.POST['status']
        app.save()
        return redirect('/show'.format(id))

def add(request):
    errors=Appointment.objects.appointment_val(request.POST)
    if "exist" in errors:
        for tag, error in errors.iteritems():
            messages.errors(request, error, extra_tags=tag)
            return redirect("/show")
    else:
        user=User.objects.get(id=request.session['user'].id)
        app= Appointment.objects.create(
            task=request.POST['task'],
            status="done",
            time=request.POST['time'],
            date=request.POST['date'],
            user=user,
        )
        return render(request, 'main/create.html')



def destroy(request, id):
    Appointment.objects.get(id=id).delete()
    return redirect('/show')

def logout(request):
    request.session.clear()
    return redirect ('/')


  