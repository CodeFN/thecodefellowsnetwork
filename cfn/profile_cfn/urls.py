from django.conf.urls import url
from profile_cfn.views import ProfileView, ProfileViewOther, EditProfileView

urlpatterns = [
    url(r'^$', ProfileView, name="profile_self"),
    url(r'^edit/$', EditProfileView.as_view(), name="edit_profile"),
    url(r'(?P<slug>[-\w]+)/$', ProfileViewOther, name="profile_other"),
]

