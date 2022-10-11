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
    user_obj = User.objects.get(username=request.user.username) # Currently logged in user_obj
    user_profile = Profile.objects.get(user=user_obj) # got the logged in user from profile using user_obj
    return render(request, 'index.html', {'user_profile': user_profile})

# User profile settings page on site
@login_required(login_url='sign-in-page')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        """
        Check if user tries to update the profile image or not
        check If image is not updated but 'bio' and 'location' updated
        check if 'image', 'bio' and 'location' are all updated
        """

        # If user doesn't update the profile image
        if request.FILES.get('profileimage') == None:        
            image = user_profile.profileimg # default-blank-image will be assigned to user
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        # If user updates the profile image
        if request.FILES.get('profileimage') != None:
            image = request.FILES.get('profileimage') # user uploaded new profile image
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})

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
                user_login = authenticate(username=username, password=password)
                login(request, user_login)

                # Create a profile object for a new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()  
                return redirect('settings')
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
    return redirect('sign-in-page')

@login_required(login_url="sign-in-page")
def upload(request):
    return HttpResponse('upload view')
