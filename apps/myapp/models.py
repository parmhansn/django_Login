from django.db import models
import re
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        if len(postData['name']) < 3:
            errors['name'] = "Name should be at least 5 characters."
        if len(postData['username']) < 3:
            errors['username'] = "Username should be at least 5 characters."
        if not postData['date_hired']:
            errors['date_hired'] = "Date hired cannot be blank"
        elif postData['date_hired'] > str(datetime.now()):
            errors['date_hired'] = "Date hired cannot be a future date"
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be less than 8 characters"
        elif postData['password'] != postData['confirm']:
            errors['password'] = "Password does not match"

        return errors

    def login_validator(self, postData):
        errors = {}

        if len(postData['username']) < 3:
            errors['username'] = "Username cannot be less than 3 characters."
        elif not User.objects.filter(username=postData['username']):
            errors['username'] = "Username does not exist"

        if len(postData['passwordlogin']) < 1:
            errors['passwordlogin'] = "password cannot be blank."
        else: 
            user= User.objects.filter(username=postData['username'])
            print(user)
            if not bcrypt.checkpw(postData['passwordlogin'].encode(), user[0].password.encode()):
                errors['passwordlogin'] = "Password does not match."

        return errors

class Wish_ListManager(models.Manager):

    def wish_list_validator(self, postData):
        errors = {}

        if len(postData['item']) < 1:
            errors['item'] = "No empty entries"
        elif len(postData['item']) < 3:
            errors['item'] = "Items should be more than 3 characters"
        return errors 

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #added_wishlists = Many to many
    #uploader = one to many


class Wish_List(models.Model):
    item = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    added_users = models.ManyToManyField(User, related_name="added_wishlists")
    uploader = models.ForeignKey(User, related_name="uploaded_wishlists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects =  Wish_ListManager()