from django.urls import reverse_lazy, reverse
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import NewUserForm, UpgradeToBloggerForm
from django.contrib import messages

from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django import template
# Create your views here.
def index(request):
    blogs = Post.objects.all()
    context = {
        'blogs':blogs
    }
    return render(request, 'index.html', context)

def sign_up(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='viewers')
            user.groups.add(group)
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('home')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context = {'form':form}
    return render(request, template_name='register.html', context=context)

def upgrade_status(request):
    form = UpgradeToBloggerForm(instance=request.user)
    if request.method == "POST":
        form = UpgradeToBloggerForm(request.POST, instance=request.user)
        # def form_valid(self,form,*kwargs):
        #     form.instance.author = self.request.user
        #     return super(upgrade_status, self).form_valid(form)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="bloggers")
            user.groups.add(group)
            group2 = Group.objects.get(name="viewers")
            user.groups.add(group2)
            messages.success(request, "User successfully upgraded.")
            return redirect('create-blog')
        messages.error(request, "Unsuccessful upgrade. Something went wrong.")
    form = UpgradeToBloggerForm(instance = request.user)
    context = {'form':form}
    return render(request, template_name='blog/upgrade_status.html', context=context)


class BlogDetailView(generic.DetailView):
    model = Post
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context["comment"] = Comment.objects.filter(post_id = self.kwargs['pk'])
        return context

    def form_valid(self, form, **kwargs):
        pass

class CommentCreateView(generic.CreateView):
    model = Comment
    fields = ['body']
    success_url = reverse_lazy('blog-detail')

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk = self.kwargs['pk'])
        return context

    def form_valid(self, form, *kwargs):
        """ Add Author and associated blog before saving"""
        # Add logged in user as the commenter
        form.instance.user = self.request.user
        # Associate the comment with the blogpost id
        form.instance.post = get_object_or_404(Post, pk = self.kwargs['pk'])
        # Add the name of the user
        form.instance.name = self.request.user.first_name
        # Call super class form validation behavior
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('blog-detail',kwargs={'pk':self.kwargs['pk']})

class BloggerListView(generic.ListView):
    model = Post
    paginate_by = 10


class BlogCreateView(generic.CreateView):
    model = Post
    fields = ['title', 'summary', 'body','genre', 'status']
    success_url = reverse_lazy('home') #TODO: May want to create a page where a blogger can view their blog posts
    #? Future idea: Add analytics to the dashboard of the blogger.

    def form_valid(self, form, *kwargs):
        """Add other details such as author"""
        # Add the author of the blog post to the form
        form.instance.author = self.request.user
        return super(BlogCreateView, self).form_valid(form)