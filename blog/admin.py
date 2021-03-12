from django.contrib import admin
from django.db import models
from django.contrib.admin.decorators import register
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
