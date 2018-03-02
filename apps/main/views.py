from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import json


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
    if 'user' in request.session:
        context = {
        'user':request.session['user'],
        "travels" : Travel.objects.all(),
        "others": Travel.objects.all().exclude(join__id=request.session['user'].id)
       }
   
        return render(request, 'main/show.html', context)
    else:
        return  redirect ('/')

def addplan(request):
    if 'user' not in request.session:
        return redirect ("/")
    else:
        print request.session['user'].id
        context= {
            "user":User.objects.get(id=request.session['user'].id),
        }
        return render(request, 'main/create.html', context)

def createplan(request):
    if request.method != 'POST':
        return redirect ("/addplan")
    newplan= Travel.objects.travelval(request.POST, request.session["user"].id)
    if newplan[0] == True:
        return redirect('/show')
    else:
        for message in newplan[1]:
            messages.error(request, message)
        return redirect('/addplan')


def join(request, travel_id):
    if request.method == "GET":
        messages.error(request,"invalid")
        return redirect('/')
    joiner= Travel.objects.join(request.session["id"], travel_id)
    
    if 'errors' in joiner:
        messages.error(request, joiner['errors'])
    return redirect('/show')


def show(request, travel_id):
    try:
        travel= Travel.objects.get(id=travel_id)
    except Travel.DoesNotExist:
        messages.info(request,"Travel Not Found")
        return redirect('/show')
    context={
        "travel": travel,
        "user":User.objects.get(id=request.session['id']),
        "others": User.objects.filter(joiner__id=travel.id).exclude(id=travel.creator.id),
    }
    return render(request, 'main/success.html', context)

def delete(request, id):
    try:
        target= Travel.objects.get(id=id)
    except Travel.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/show')
    target.delete()
    return redirect('/show')


def logout(request):
    request.session.clear()
    return redirect ('/')


  