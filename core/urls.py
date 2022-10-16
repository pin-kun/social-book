from unicodedata import name
from django.urls import path
from core.views import *

urlpatterns = [
    path('', home, name="home-page"),
    path('signup/', signup, name='sign-up-page'),
    path('signin/', signin, name='sign-in-page'),
    path('logout/', logout_view, name='logout-view'),
    path('settings/', settings, name='settings'),

    path('upload/', upload, name='upload'),
    path('profile/<str:pk>/', profile, name='profile'),
    # path('settings/profile/', profile, name='settings-profile'),
    path('like-post/', like_post, name='like-post'),
    path('follow/', follow, name='follow'),
    path('search/', search, name='search-username'),
]