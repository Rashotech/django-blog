from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from blog_posts.models import BlogPost, Category

def homepage(request):
    posts_list = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'homepage.html', { 'page_obj': page_obj, 'categories': categories })