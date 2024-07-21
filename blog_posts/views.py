from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import BlogPost, Category
from django.contrib.auth.decorators import login_required
from . import forms 

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
    comments = post.comments.filter(post=post).order_by('-created_at')
    form = forms.CommentForm(request.POST)
    return render(request, 'blog_posts/single_post.html', {'post': post, 'comments': comments, 'form': form})

def search(request):
    query = request.GET.get('q')
    posts_list = BlogPost.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by('-created_at')    
    paginator = Paginator(posts_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'homepage.html', {'page_obj': page_obj, 'categories': categories, 'search_query': query})

@login_required(login_url="/users/login/")
def create_blog_post(request):
    if request.method == 'POST': 
        form = forms.CreatePost(request.POST) 
        if form.is_valid():
            newpost = form.save(commit=False) 
            newpost.author = request.user 
            newpost.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('/')
        else:
            messages.error(request, 'Unable to create blog post.')
    else:
        form = forms.CreatePost()
    return render(request, 'blog_posts/new_post.html', { 'form': form })

@login_required(login_url="/users/login/")
def edit_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.author != request.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('/')
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('/')
        else:
            messages.error(request, 'Failed to update post.')
    else:
        form = forms.CreatePost(instance=post)
    return render(request, 'blog_posts/edit_post.html', {'form': form, 'post': post})

def create_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, id=post_id)
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('posts:single_post', post_id=post.id)
        else:
            messages.error(request, 'Failed to add comment. Please try again later.')