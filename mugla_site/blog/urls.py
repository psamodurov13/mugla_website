from django.urls import path

from .views import *

urlpatterns = [
    path('', Blog.as_view(), name='blog'),
    # path('create-post/', CreatePost.as_view(), name='create_post'),
    path('create-post/', create_post_ajax, name='create_post_ajax'),
    path('category/<str:slug>/', CategoryPost.as_view(), name='category'),
    path('tag/<str:slug>/', TagPost.as_view(), name='tag'),
    path('posts/<str:slug>/', PostPage.as_view(), name='post'),
    path('<str:slug>/', CityPost.as_view(), name='city_post'),
    path('news/user/<str:slug>/', UserNews.as_view(), name='user_news'),
    path('articles/user/<str:slug>/', UserArticles.as_view(), name='user_articles'),
    path('search/', Search.as_view(), name='search'),
]