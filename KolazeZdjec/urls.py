"""KolazeZdjec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from CollageMaker import views
from KolazeZdjec.settings import MEDIA_URL
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from KolazeZdjec import settings

urlpatterns = [
    path("", views.index, name="index"),
    # path('generated_collage', views.generate_collage, name='generate_collage'),
    path("api/check_url", views.check_url, name="check_url"),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
