from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomeUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    # This part tells the admin which fields to show in the edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('phone', 'is_verified')}),
    )
    # This part tells the admin which fields to show in the creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra', {'fields': ('email', 'phone')}),
    )
    ordering = ('email',)