"""family_organiser URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'family_organiser.views.error_404'
handler500 = 'family_organiser.views.error_500'
handler403 = 'family_organiser.views.error_403'
handler400 = 'family_organiser.views.error_400'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('user/', include('user.urls')),
    path('status/', include('status.urls')),
    path('shopping/', include('shopping.urls')),
    path('premium/', include('premium.urls')),
    path('message/', include('message.urls')),
    path('event/', include('event.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   

