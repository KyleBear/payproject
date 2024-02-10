"""payhere_project URL Configuration

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
from payproject.views import ProductListView, ProductDetailView
from payproject.views import OwnerSignupView, OwnerLoginView
from payproject.views import search_product, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/list', ProductListView.as_view(), name='product-list'),
    # path('api/products/detail', ProductDetailView.as_view(), name='product-list'),
    path('api/owner/signup/', OwnerSignupView.as_view(), name='owner-signup'),
    path('api/owner/login/', OwnerLoginView.as_view(), name='owner-login'),
    path('api/products/detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/products/search/<str:keyword>', search_product, name='search_product'),
    path('api/logout/', LogoutView.as_view(), name='logout'), # 로그아웃 URL 설정
     # 상세조회,
     
     ]
