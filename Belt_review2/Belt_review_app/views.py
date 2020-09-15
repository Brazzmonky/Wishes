from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt


def login_reg(request):
	return render(request, 'login.html')


def newUser(request):
	errors = User.objects.register_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		password=request.POST['password']
		pw_hash= bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		newUser=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash.decode())
		context={
		"users": User.objects.all()	
		}
		request.session['loggedinUserID'] = newUser.id
		return redirect('/home')


def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		loggedinUser = User.objects.get(email=request.POST['email'])
		request.session['loggedinUserID'] = loggedinUser.id
		return redirect('/home')


def home(request):
	loggedinUser= User.objects.get(id=request.session['loggedinUserID'])
	user_wishes =Wish.objects.filter(user=loggedinUser)
	context={
	"user_wishes": user_wishes,
	"all_users": User.objects.all(),
	"all_wishes": Wish.objects.all(),
	"loggedinUser": User.objects.get(id=request.session['loggedinUserID'])
	}
	return render(request, "home.html", context)

def wish(request,userid):
	loggedinUser=User.objects.get(id=request.session['loggedinUserID'])
	context={
	"loggedinUser":loggedinUser,
	}
	return render(request, "addwish.html", context)


def makewish(request,userid):
	errors = Wish.objects.wish_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/makewish/" + str(userid))
	else:		
		loggedinUser=User.objects.get(id=userid)
		Wish.objects.create(item=request.POST['item'], description=request.POST['description'],user=loggedinUser)
		return redirect("/home")

def grant(request,wishid):
	wish_to_update=Wish.objects.get(id=wishid)
	wish_to_update.granted=(True)
	wish_to_update.save()
	return redirect("/home")

def boop(request,wishid):
	wish_to_delete=Wish.objects.get(id=wishid)
	wish_to_delete.delete()
	return redirect('/home')

def editwish(request,wishid):
	wish_to_edit=Wish.objects.get(id=wishid)
	loggedinUser=User.objects.get(id=request.session['loggedinUserID'])
	context={
	"loggedinUser":loggedinUser,
	"wish_to_edit":wish_to_edit,
	}
	return render(request,'editwish.html', context)

def edit(request,wishid):
	wish_to_edit=Wish.objects.get(id=wishid)
	wish_to_edit.item=request.POST['item']
	wish_to_edit.description=request.POST['description']
	wish_to_edit.save()
	return redirect('/home')

def stats(request,userid):
	loggedinUser=User.objects.get(id=userid)
	wishes =Wish.objects.filter(user=User.objects.get(id=userid))
	context={
	"wishes":wishes,
	"loggedinUser": loggedinUser,
	}
	return render(request,'stats.html', context)

def logout(request):
	request.session.clear()
	return redirect("/")
	