from django.conf.urls import url
from profile_cfn.views import ProfileCfnView

urlpatterns = [
    url(r'^$', ProfileCfnView.as_view(), name="profile_cfn"),
]
