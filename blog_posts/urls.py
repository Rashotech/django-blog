from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('author/<int:author_id>/', views.author_filter, name='author_filter'),
    path('category/<int:category_id>/', views.category_filter, name='category_filter'),
    path('<int:post_id>/', views.single_post, name='single_post'),
    path('<int:post_id>/edit/', views.edit_blog_post, name='edit_blog_post'),
    path('search/', views.search, name='search'),
    path('new/', views.create_blog_post, name='create_blog_post'),
]