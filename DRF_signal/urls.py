"""DRF_Applcation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/posts/', views.user_lst, name='post-lst'),
    path('api/posts/<int:pk>/', views.user_dtl, name='post-dtl'),
    path('api/get-blocked-user/', views.BlockedUser_lst, name='get-blocked-user'),
    path('api/block-user/', views.BlockedUser_lst, name='block-user'),
    path('api/unblock-user/', views.BlockedUser_lst, name='unblock-user'),
]


