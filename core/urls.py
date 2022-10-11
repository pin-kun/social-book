from unicodedata import name
from django.urls import path
from core.views import home, signup, signin, logout_view

urlpatterns = [
    path('', home, name="home-page"),
    path('signup/', signup, name='sign-up-page'),
    path('signin/', signin, name='sign-in-page'),
    path('logout/', logout_view, name='logout-view'),
]