from django.contrib import admin
from core.models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'id_user', 'bio', 'profileimg', 'location']
admin.site.register(Profile, ProfileAdmin)
