from unicodedata import name
from django.urls import path
from core.views import home, signup

urlpatterns = [
    path('', home, name="home"),
    path('signup/', signup, name='sign-up')
]