from __future__ import unicode_literals
from django.db import models
import re, bcrypt



class UserManager(models.Manager):
	def register_validator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors= {}
		validemail=User.objects.filter(email=postData['email'])
		if len(validemail) > 0:
			errors['email']="Email already in use. Please log in or choose another"
		if not EMAIL_REGEX.match(postData['email']):           
			errors['email'] = "Invalid email address!"	
		if len(postData ['first_name']) < 2:
			errors['first_name'] = "Required field, please input a name of at least 2 letters"
		if len(postData ['last_name']) < 2:
			errors['last_name'] = "Required field, please input a name of at least 2 letters"
		if len(postData ['password']) < 8:
			errors['password']= "Required field, please input a password of at least 8 characters"
		if postData['password']	!= postData['confirmpw']:
			errors['confirmpw']= "Passwords must match"
		return errors


	def login_validator(self,postData):
		useremail=User.objects.filter(email=postData['email'])
		errors= {}
		if len(postData['email']) == 0:
			errors['emaillen']= "Required field please enter a valid email."
		if len(useremail) < 1:
			errors['email']="No Email matching that address, please register or try another Email."
		else:
			print(useremail)
			user=User.objects.get(email=postData['email'])	
			if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
				print("password match")
			else:
				errors['passwordfailed']= "Incorrect password, please try again."
				print("failed password")
		return errors


class User(models.Model):
	first_name=models.CharField(max_length=255)
	last_name=models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	objects = UserManager()
	def __repr__ (self):
		return f"User: {self.first_name} {self.last_name} {self.email} ({self.created_at}) ({self.updated_at})"


class WishManager(models.Manager):
	def wish_validator(self,postData):
		errors={}
		if len(postData['item']) < 3:
			errors['item']= "Please enter a Wish."
		if len(postData['description']) < 10:
			errors['description']="Please enter a description of at least ten characters."	
		return errors	

class Wish(models.Model):
	item=models.CharField(max_length=255)
	description=models.CharField(max_length=255)
	granted=models.BooleanField(default=False)
	user=models.ForeignKey(User, related_name="wish", on_delete=models.CASCADE, default=None, null=True)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	objects = WishManager()
	def __repr__(self):
		return f"{self.item} {self.description} {self.granted} {self.user} ({self.created_at}) ({self.updated_at})"