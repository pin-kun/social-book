from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() # Will always return currently logged in user

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=10, blank=True)

    # dunder function - Just for admin panel visibility
    def __str__(self):
        return self.user.username