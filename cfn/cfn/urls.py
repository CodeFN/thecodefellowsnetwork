"""cfn URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from cfn.views import HomeView, FindUserView, AboutView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^registration/', include('registration.backends.hmac.urls')),
    url(r'^login/', auth_views.login, {'next_page': '/'}, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^profile/', include('profile_cfn.urls')),
    url(r'^find/users/', FindUserView.as_view(), name='find_users'),
    url(r'^posts/', include('posts.urls')),
    url(r'^about/', AboutView.as_view(), name='about'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
