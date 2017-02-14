from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from profile_cfn.models import ProfileCfn
from profile_cfn.views import ProfileView
import factory


# class UserFactory(factory.django.DjangoModelFactory):
#     """User factory for testing."""

#     class Meta:
#         """Model meta."""

#         model = User

#     username = factory.Sequence(lambda n: "User{}".format(n))
#     email = factory.LazyAttribute(
#         lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
#     )


# class BackendTests(TestCase):
#     """User/profile backend test runner."""

#     def setUp(self):
#         """Set up for backend test runner."""
#         self.users = [UserFactory.create() for i in range(5)]

#     def test_profile_is_made_when_user_is_saved(self):
#         """Test profile created when user is registered."""
#         self.assertTrue(ProfileCfn.objects.count() == 5)

#     def test_profile_is_associated_with_users(self):
#         """Test profile has correct user instance."""
#         profile = ProfileCfn.objects.first()
#         username = self.users[0].username
#         self.assertTrue(profile.user.username == username)


class FrontendTests(TestCase):
    """User/profile frontend test runner."""

    def setUp(self):
        """Set up for frontend fest runner."""
        self.client = Client()
        self.request = RequestFactory()

    # def add_user(self):
    #     """Make a user and return his profile."""
    #     user = UserFactory.create()
    #     user.username = 'test_user'
    #     user.set_password('testpassword')
    #     user.save()
    #     return user

    def test_profile_view_returns_status_ok(self):
        """Test profile view returns status code 200."""
        response = self.client.get("/profile/")
        self.assertTrue(response.status_code == 200)
