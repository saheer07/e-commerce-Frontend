"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include  # include is used to include app URLs
from django.conf import settings              # ✅ add this line
from django.conf.urls.static import static 
  # ✅ and this one


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
      # REST Auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # Social Auth (Google/Facebook)
    path('dj-rest-auth/google/', include('allauth.socialaccount.providers.google.urls')),
    path("api/orders/", include("orders.urls")),
    path('api/reviews/', include('reviews.urls')),
    path('api/wishlist/', include('wishlist.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
