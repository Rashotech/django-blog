from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import BlogPost, Category

def category_filter(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts_list = BlogPost.objects.filter(category=category).order_by('-created_at')
    paginator = Paginator(posts_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'homepage.html', {'page_obj': page_obj, 'categories': categories, 'selected_category': category})

def author_filter(request, author_id):
    author = get_object_or_404(User, id=author_id)
    posts_list = BlogPost.objects.filter(author=author).order_by('-created_at')
    paginator = Paginator(posts_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'homepage.html', { 'page_obj': page_obj, 'categories': categories, 'author': author })

def single_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blog_posts/single_post.html', { 'post': post })

def search(request):
    query = request.GET.get('q')
    posts_list = BlogPost.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by('-created_at')    
    paginator = Paginator(posts_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'blog_posts/search_results.html', {'page_obj': page_obj, 'categories': categories, 'search_query': query})