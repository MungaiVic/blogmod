from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#? using django-countries, we can add another field for countries(check documentation for extra ideas here:
#? https://pypi.org/project/django-countries/#description)


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, last_name, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide a valid email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, user_name, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)
        # Checking for wrong values
        if other_fields.get('is_staff') is not True:
            raise ValueError(_("Super User must be assigned to is_staff=True"))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_("Super User must be assigned to is_superuser=True"))
        if other_fields.get('is_active') is not True:
            raise ValueError(_("Super User must be assigned to is_active=True"))
        return self.create_user(email, user_name, first_name, last_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    user_name = models.CharField(max_length=150, unique=True, help_text=_("Enter pseudonym"))
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default = timezone.now)
    bio = models.TextField(_("Bio"), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    def __str__(self):
        return self.user_name



class Post(models.Model):
    STATUS_CHOICES = (
            ("draft", "Draft"),
            ("published", "Published"),
        )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    summary = models.TextField(max_length=500, help_text="Give a brief summary of what your post is about")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    genre = models.ForeignKey('Tag',null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft"
    )

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    """Model representing a comment"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(max_length=160)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return "Comment by {} on {}".format(self.name, self.post)


class Tag(models.Model):
    """Model representing a post genre."""
    name = models.CharField(max_length=200, help_text='Enter the category of your blog post (e.g Business, self help...)')

    def __str__(self):
        """String for representing model tag/genre"""
        return self.name

