from django.urls import path

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('blog', Blog.as_view(), name='blog'),
    path('category/<str:slug>/', CategoryPost.as_view(), name='category'),
    path('tag/<str:slug>/', TagPost.as_view(), name='tag'),
    path('posts/<str:slug>/', PostPage.as_view(), name='post'),
    path('blog/<str:slug>/', CityPost.as_view(), name='city_post')
]