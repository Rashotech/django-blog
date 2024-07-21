from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.contrib import messages
from blog_posts.models import BlogPost
from .models import UserUpdateForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            login(request, form.save())
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", { "form": form })

def login_view(request): 
    if request.method == "POST": 
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            print(form)
            login(request, form.get_user())
            return redirect("/") 
    else: 
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form })

def logout_view(request):
    if request.method == "POST": 
        logout(request) 
        return redirect("/")
    
@login_required(login_url="/users/login/")
def profile_view(request): 
    posts_list = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(posts_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'page_obj': page_obj, 'form': form})

@login_required(login_url="/users/login/")
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Failed to update profile.')