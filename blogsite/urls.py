from django.contrib import admin
from django.urls import include, path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('users/', include('users.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
