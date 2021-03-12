from django.db import models
from django.contrib.auth.models import Permission, User
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

# Create your models here.
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
        # content_type = ContentType.objects.get_for_model('Post')
        # permission = Permission.objects.create(
        #     codename='can_publish',
        #     name = 'Can Publish Posts',
        #     content_type = content_type,
        #)

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
