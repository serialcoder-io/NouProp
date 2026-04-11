from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Role, User


# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']

class UserAdmin(admin.ModelAdmin): # type: ignore
    list_display = ['display_name', 'email', 'role']


admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)