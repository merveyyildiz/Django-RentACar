"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views

urlpatterns = [
    path("", include("home.urls")),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'), #ilki fonsiyon tanımladık ikincisi fonk adını belirtir
    path('referanslar/', views.referanslarimiz, name='referanslarimiz'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path("product/", include("product.urls")),
    path('admin/', admin.site.urls),  # admin şifre merve
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<int:id>/<slug:slug>/', views.category_products, name="category_products"),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name="product_detail")
]


if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #media url ve root görünür olmasını sağlıyor


