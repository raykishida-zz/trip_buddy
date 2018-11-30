from __future__ import unicode_literals
from django.db import models
import re
import bcrypt 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def user_validation(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = 'First name is required'
        elif postData['first_name'].isalpha() == False:
            errors['first_name'] = 'Invalid characters in first name'

        if len(postData['last_name']) < 1:
            errors['last_name'] = 'Last name is required'
        elif postData['last_name'].isalpha() == False:
            errors['last_name'] = 'Invalid characters in last name'

        if len(postData['email_reg']) < 1:
            errors['email_reg'] = 'Email is required'
        elif not EMAIL_REGEX.match(postData['email_reg']):
            errors['email_reg'] = 'Email is invalid'
        elif User.objects.filter(email=postData['email_reg']).exists():
            errors['email_reg'] = 'Email already exists'

        if len(postData['password_reg']) < 1:
            errors['password_reg'] = 'Password is required'
        elif len(postData['password_reg']) < 8:
            errors['password_reg'] = 'Password must be at least 8 characters'

        if postData['password_reg'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'

        print('Registration errors', errors)
        return errors


    def login_validation(self, postData):
        errors = {}
        try: 
            if User.objects.get(email=postData['email_login']) and bcrypt.checkpw(postData['password_login'].encode(), User.objects.get(email=postData['email_login']).password.encode()) == True:
                pass
            else:
                errors['login'] = 'Login Failed'
        except: 
            errors['login'] = 'Login Failed'
        print('Login_validation errors: ',errors)
        return errors

class TripManager(models.Manager):
    def trip_validation(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destination'] = 'Destination is required'

        if len(postData['description']) < 1:
            errors['description'] = 'Description is required'

        if len(postData['travel_date_from']) < 1:
            errors['travel_date_from'] = 'Date required'
        if len(postData['travel_date_to']) < 1:
            errors['travel_date_to'] = 'Date required'
        elif postData['travel_date_to'] < postData['travel_date_from']:
            errors['travel_date_to'] = 'Travel Date From must be before Travel Date To'

        return errors    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_trip')
    joined_by = models.ManyToManyField(User, related_name='joined_trip')

    objects = TripManager()