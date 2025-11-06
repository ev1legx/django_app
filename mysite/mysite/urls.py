"""
URL configuration for mysite project.

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
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from shopapp.views import example_view
from django.contrib.sitemaps.views import sitemap
from shopapp.views import ShopSitemap, LatestProductsFeed

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('shop/', include('shopapp.urls')),
    path('accounts/', include('myauth.urls')),
    path('', include('shopapp.urls')),
    # Добавляем пути для drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    #sitemap and RSS
path('sitemap.xml', sitemap, {'sitemaps': {'shop': ShopSitemap}}, name='sitemap'),
    path('products/latest/feed/', LatestProductsFeed(), name='latest-products-feed'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('shop/', include('shopapp.urls')),
    path('accounts/', include('myauth.urls')),
    path('blog/', include('django_blog.urls')),
    path('test/', example_view),

)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)