from django.conf.urls import url
from profile_cfn.views import ProfileView, ProfileViewOther

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name="profile_self"),
    url(r'(?P<slug>\w+)/$', ProfileViewOther.as_view(), name="profile_other"),
]
