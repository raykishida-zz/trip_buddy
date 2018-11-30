from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'trip_buddy/index.html')

def register(request):
    errors = User.objects.user_validation(request.POST)
    print('*'*80, 'Registration POST', request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email_reg'], password=bcrypt.hashpw(request.POST['password_reg'].encode(), bcrypt.gensalt()))
        request.session['user_id'] = User.objects.get(email=request.POST['email_reg']).id
        return redirect('/travels')

def login(request):
    errors = User.objects.login_validation(request.POST)
    print('*'*80, 'Login POST', request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email=request.POST['email_login']).id
        return redirect('/travels')

def dashboard(request):
    if 'user_id' in request.session:
        context = {
            'user_info': User.objects.get(id=request.session['user_id']),
            'user_trips': Trip.objects.filter(joined_by=request.session['user_id']), #Trip.objects.filter(created_by=request.session['user_id'])|
            'other_trips': Trip.objects.exclude(joined_by=request.session['user_id']) #.exclude(created_by=request.session['user_id']))
   }
        return render(request, 'trip_buddy/dashboard.html', context)
    else:
        return redirect('/')

def detail(request, id):
    context = {
        'trip_detail': Trip.objects.get(id=id),
        'others': Trip.objects.get(id=id).joined_by.values(),
        'created_by': Trip.objects.get(id=id).created_by.id
    }
    print(context)
    return render(request, 'trip_buddy/details.html', context)

def addtrip(request):
    return render(request, 'trip_buddy/addtrip.html')

def create(request):
    errors = Trip.objects.trip_validation(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addtrip')
    else:
        Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], travel_date_from=request.POST['travel_date_from'], travel_date_to=request.POST['travel_date_to'], created_by=User.objects.get(id=request.session['user_id'])) 
        trip = Trip.objects.get(destination=request.POST['destination'])
        user = User.objects.get(id=request.session['user_id'])
        trip.joined_by.add(user)
        return redirect('/travels')

def join(request, id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    trip.joined_by.add(user)
    return redirect('/travels')

def cancel(request, id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    trip.joined_by.remove(user)
    return redirect('/travels')

def delete(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect('/travels')

def logout(request):
    del request.session['user_id']
    return redirect('/')
