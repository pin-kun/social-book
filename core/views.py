from itertools import chain
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core.models import FollowersCount, LikePost, Post, Profile
import random

# Home Page
@login_required(login_url='sign-in-page') # If user is not logged in then, user will be sent to login page
def home(request):
    user_obj = User.objects.get(username=request.user.username) # Currently logged in user_obj
    user_profile = Profile.objects.get(user=user_obj) # got the logged in user from Profile Model using user_obj
    user_post = Post.objects.filter(user=user_obj).order_by('-created_at') # ALl the posts of currently logged in user, In Descending order by DateTime

    # get the following user(s) of currently logged in user
    following_user_list = []
    following_user_feed_list = []
    following_user_usernames = []

    following_user = FollowersCount.objects.filter(follower=user_obj) # list of all the users whome currently logged in user is already following
    # print(following_user)

    for users in following_user:
        following_user_list.append(users)
        following_user_usernames.append(users.user)
    
    
    for usernames in following_user_list:
        user_feed_lists =  Post.objects.filter(user=usernames)
        following_user_feed_list.append(user_feed_lists)    
    
    feed_list = list(chain(*following_user_feed_list))

    # print('fedd list-->', len(following_user_list))

    # for suggestions to follow other accounts
    all_users = User.objects.all() # all the users on the plateform
    user_following_all = [] # list of all the users whome currently logged in user is already following

    for user in following_user:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    # removing the common user(s) and filtering out only those users who are not followed by currently logged in user
    # we can't recommend ourself to ourself. so we are not removing ourself from suggestion list
    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))] 
    currently_user = User.objects.filter(username=request.user.username) 
    final_suggestion_list =  [x for x in list(new_suggestion_list) if (x not in list())]
    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []
    
    for users in final_suggestion_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
    
    suggestion_username_profile_list = list(chain(*username_profile_list))

    context = {
        'user_profile': user_profile,
        'user_post': feed_list,
        'following_user_post': '',
        'suggestion_username_profile_list': suggestion_username_profile_list[:4] # only first 4 suggestions from the list
    }
    return render(request, 'index.html', context=context)


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
def profile(request, pk):
    # This will be used when someone clicks on "username" on the post, It will redirect to the profile page of that user who posted the pic
    user_obj = User.objects.get(username=pk) # get the user using the pk
    profile_obj = Profile.objects.get(user=user_obj) # get the user of the post from "Profile" model
    user_posts = Post.objects.filter(user=pk) # get all the posts of the user whose id=pk
    user_post_length = len(user_posts) # length of all the posts of the user

    # Here pk = user whose profile is opened on the page
    logged_in_follower = request.user.username # user who is logged in and following
    profile_user = pk # user, whose profile is being viewed currently

    # if logged in user is following user then show "Following" else show "Unfollow"
    if FollowersCount.objects.filter(follower=logged_in_follower, user=profile_user).first():
        follow_button_text = "Unfollow"
    else:
        follow_button_text = "Follow"
    
    # get the length of the "user" from "FollowersCount" table where user=pk (currently opened profile page)
    # It means "no. of times, the user of the currently opened profile page is shown in 'user' list in 'FollowersCount' table"
    # That many time current profile_page user has been followed by the "other users"
    user_followers = len(FollowersCount.objects.filter(user=pk))

    # get the length of the "follower" from "FollowersCount" table where user=pk (currently opened profile page)
    # It means "no. of times, the user of the currently opened profile page is shown in 'follower' list in 'FollowersCount' table"
    # That many time current profile_page user has been following the "other users"
    user_following = len(FollowersCount.objects.filter(follower=pk))         

    context = {
        'user_obj': user_obj,        
        'profile_obj': profile_obj,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'follow_button_text': follow_button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }

    return render(request, 'profile.html', context=context)

@login_required(login_url="sign-in-page")
def upload(request):
    # if image uploaded then post it else return directly to home page
    if request.method == "POST":
        # get the data
        user = request.user.username # Current logged in user's username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        # save it to the Post model (in database)
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect("/", )
    else:
        return redirect("/")
                                                                                                                 
@login_required(login_url='sign-in-page')
def like_post(request):
    current_username = request.user.username # Currently logged in user
    post_id = request.GET.get('post_id') # post_id of liked post

    post_obj = Post.objects.get(id=post_id) # getting the post_obj of post_id from "Post" model

    # Check whether the current logged in user already liked this post or not?
    # If not liked then increase the no_of_likes of post else delete the like and liked_object
    like_filter = LikePost.objects.filter(post_id=post_id, username=current_username).first()

    # If there is no "current_username" found against this "post_id" then increase the like of the post 
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=current_username)
        new_like.save()
        post_obj.no_of_likes += 1 # increase the likes of the post in "Post" model
        post_obj.save()
        return redirect("/")
    else:
        like_filter.delete() # delete the "like_filter" object from "LikePost" model, since user has already liked this post
        post_obj.no_of_likes -= 1 # Decrease the likes for the post
        post_obj.save()
        return redirect("/")

@login_required(login_url='sign-in-page')
def follow(request):
    if request.method == "POST":
        follower = request.POST['follower'] # currently logged in user
        user = request.POST['user'] # user, whose profile is being viewed by currently logged in user

        is_already_followed = FollowersCount.objects.filter(follower=follower, user=user).first()

        if is_already_followed:
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete() # basically unfollow
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect("/profile/"+user)

    else:
        return redirect("/")

@login_required(login_url='sign-in-page')
def search(request):
    if request.method == "POST":
        user_obj = User.objects.get(username=request.user.username) # Currently logged in user_obj
        user_profile = Profile.objects.get(user=user_obj) # got the logged in user from Profile Model using user_obj

        searched_username = request.POST['search_username']
        username_obj = User.objects.filter(username__icontains=searched_username)

        username_profile = []
        username_profile_list = []
        
        for users in username_obj:
            username_profile.append(users.id) # here we are appending the "id", you can do without "id" too
        
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
        print('test---->>', username_profile_list)

        context = {
            'searched_username': searched_username,
            'user_profile': user_profile,
            'username_profile_list': username_profile_list
        }
    return render(request, 'search.html', context=context)
