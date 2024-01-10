"""ecom URL Configuration

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
from tabnanny import verbose
from django.contrib import admin
from django.urls import path, include
# from django.urls import re_path as url
from django.urls import path as url

from django.conf import settings
# from django.conf.urls.i18n import i18n_patterns
from home import views


# from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.contrib.auth import views as auth_views

# from django.conf.urls import handler400, handler403, handler404, handler500

# handler400 = "home.views.bad_request"
# handler403 = "home.views.permission_denied"
# handler404 = "home.views.page_not_found"
# handler500 = "home.views.server_error"

urlpatterns = [
    path("boss/", admin.site.urls),
    path("", include("home.urls")),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
