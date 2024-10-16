"""
URL configuration for myShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
#from users.views import UserRegistrationView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, CategoryViewSet, ProductImageViewSet, PromotionViewSet, WishlistViewSet, ReviewViewSet, APIDocumentationView
from rest_framework_simplejwt.views import TokenObtainPairView


router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='product')
router.register(r'reviews', ReviewViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'wishlist', WishlistViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'promotions', PromotionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', TokenObtainPairView.as_view(), name='auth'),
    path('api/documentation/', APIDocumentationView.as_view(), name='api-docs'),
    #path('register/', UserRegistrationView.as_view(), name='register'),
    #path('api/v1/', include('products.urls'))
]
