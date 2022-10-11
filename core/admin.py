from django.contrib import admin
from core.models import Profile, Post

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'id_user', 'bio', 'profileimg', 'location']
admin.site.register(Profile, ProfileAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'image', 'caption', 'created_at', 'no_of_likes']
admin.site.register(Post, PostAdmin)
