"""hgworker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from qyweixin import views as qy_views
from . import views
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/', qy_views.test),
    url(r'^WW_verify_ezMdV9DUy3dH4ilP.txt', views.txt),
    #url(r'^(?P<path>WW_verify_ezMdV9DUy3dH4ilP.txt)$', 'django.views.static.serve', {'document_root': settings.BASE_DIR}),
    url(r'^discount/', include('discount.urls', namespace="qrcode")),
    url(r'^userinfo/', include('userinfo.urls', namespace="userinfo")),
    url(r'^report/', include('report.urls', namespace="report")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)

