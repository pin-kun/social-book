from django.contrib import admin
from core.models import FollowersCount, LikePost, Profile, Post

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'id_user', 'bio', 'profileimg', 'location']
admin.site.register(Profile, ProfileAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'image', 'caption', 'created_at', 'no_of_likes']
admin.site.register(Post, PostAdmin)

class LikePostAdmin(admin.ModelAdmin):
    list_display = ["post_id", "username"]
admin.site.register(LikePost, LikePostAdmin)

class FollowersCountAdmin(admin.ModelAdmin):
    list_display = ['follower', 'user']
admin.site.register(FollowersCount, FollowersCountAdmin)