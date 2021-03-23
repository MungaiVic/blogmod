from django.contrib import admin
from django.db import models
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@register(Post)
class PostInline(admin.ModelAdmin):
    model = Post
    inlines = [CommentInline]


class UserAdminConfig(UserAdmin):
    """We are customizing the admin area for the users
    """
    # Adding some search fields
    search_fields = ('email', 'user_name', 'first_name',)
    #Adding some filtering capabilities
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    # Defining the ordering
    ordering = ('-start_date',)
    # Defining what we want to display using the list_display
    list_display = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')

    fieldsets = (
        (None, {"fields": ('email', 'user_name', 'first_name',)}),# This is the top section
        ('Permissions', {'fields': ( 'is_active', 'is_staff')}),# Permissions section
        ('Personal',{'fields': ('bio',)}),# Personal info section
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(User,UserAdminConfig)