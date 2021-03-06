from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('blogs', views.blogs, name='blogs'),
    path('register', views.sign_up, name='register'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blog/<int:pk>/create', views.CommentCreateView.as_view(), name='comment'),
    path('create-blog', views.BlogCreateView.as_view(), name='create-blog'),
    path('upgrade-status', views.upgrade_status, name='upgrade-status'),
    path('blogger-list', views.blogger_list, name='blogger-list'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-info')
]
