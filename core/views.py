from curses import use_default_colors
from platform import java_ver
import re
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core.models import Profile

# Home Page
@login_required(login_url='sign-in-page') # If user is not logged in then, user will be sent to login page
def home(request):
    # If user is not logged in or not autheticated
    # if not request.user.is_authenticated:
    #     return redirect('sign-in-page')
    return render(request, 'index.html')

# SignUp Page
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # password match condition
        if password == password2:
            if User.objects.filter(email=email).exists():
                # If email already exists
                messages.info(request, "Email is already taken")
                return redirect('sign-up-page')
            elif User.objects.filter(username=username).exists():
                # If username already exists
                messages.info(request, "Username is already taken")
                return redirect('sign-up-page')
            else:
                # If email and username don't exists then create user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in  and redirect to settings page

                # Create a profile object for a new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()  
                return redirect('sign-up-page')
        else:
            messages.info(request, "Password not matching. Please type the same password")
            return redirect('sign-up-page')
    else:
        return render(request, 'signup.html')

# SignIn Page
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authentication of existing user
        check_if_user_exists = User.objects.filter(username=username).exists()

        if check_if_user_exists:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # This user is authenticated and valid
                login(request, user)
                print('username', username)
                return redirect('/')
            else:
                # Not a valid user. Wrong passwrod
                messages.info(request, 'Wrong passwrod. Please try again')
                return redirect('sign-in-page')
        else:
            # There is no such user in the database
            messages.info(request, "Username not found. Please check your username")
            return redirect('sign-in-page')

    return render(request, 'signin.html')

@login_required(login_url='sign-in-page ')
def logout_view(request):
    logout(request)
    print('logout user', request.user)
    return redirect('sign-in-page')
