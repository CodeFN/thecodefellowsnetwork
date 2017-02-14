from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from profile_cfn.models import ProfileCfn
from profile_cfn.views import ProfileView
import factory


class UserFactory(factory.django.DjangoModelFactory):
    """User factory for testing."""

    class Meta:
        """Model meta."""

        model = User

    username = factory.Sequence(lambda n: "User{}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
    )


class BackendTests(TestCase):
    """User/profile backend test runner."""

    def setUp(self):
        """Set up for backend test runner."""
        self.users = [UserFactory.create() for i in range(5)]

    def test_profile_is_made_when_user_is_saved(self):
        """Test profile created when user is registered."""
        self.assertTrue(ProfileCfn.objects.count() == 5)

    def test_profile_is_associated_with_users(self):
        """Test profile has correct user instance."""
        profile = ProfileCfn.objects.first()
        username = self.users[0].username
        self.assertTrue(profile.user.username == username)


class FrontendTests(TestCase):
    """User/profile frontend test runner."""

    def setUp(self):
        """Set up for frontend fest runner."""
        self.client = Client()
        self.request = RequestFactory()

    def add_user(self):
        """Make a user and return his profile."""
        user = UserFactory.create()
        user.username = 'test_user'
        user.set_password('testpassword')
        user.save()
        return user

    def test_profile_view_authenticated_returns_status_ok(self):
        """Test profile view returns status code 200."""
        self.add_user()
        self.client.login(username='test_user', password='testpassword')
        response = self.client.get('/profile', follow=True)
        self.assertTrue(response.status_code == 200)

    def test_profile_view_unauthenticated_returns_status_redirect(self):
        """Test profile view with unauthenticated client returns status code 302."""
        response = self.client.get("/profile/")
        self.assertTrue(response.status_code == 302)

    def test_other_profile_view_authenticated_returns_status_ok(self):
        """Test other profile view with authenticated client returns status code 200."""
        self.add_user()
        self.client.login(username='test_user', password='testpassword')
        new_user = UserFactory.create()
        response = self.client.get('/profile/' + new_user.username, follow=True)
        self.assertTrue(response.status_code == 200)

    def test_other_profile_view_unauthenticated_returns_status_redirect(self):
        """Test other profile view with unauthenticated client returns status code 301."""
        self.add_user()
        response = self.client.get("/profile/test_user")
        self.assertTrue(response.status_code == 301)

    def test_no_profile_authenticated_returns_status_not_found(self):
        """Test non-existing profile view with unauthenticated client returns status code 302."""
        self.add_user()
        self.client.login(username='test_user', password='testpassword')
        response = self.client.get("/profile/abcdefg")
        self.assertTrue(response.status_code == 301)

    def test_no_profile_unauthenticated_returns_status_redirect(self):
        """Test non-existing profile view with unauthenticated client returns status code 302."""
        response = self.client.get("/profile/abcdefg")
        self.assertTrue(response.status_code == 301)

    def test_profile_route_uses_correct_template(self):
        """Test that the profile view renders the profile.html template."""
        self.add_user()
        self.client.login(username='test_user', password='testpassword')
        response = self.client.get("/profile/")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "profile_cfn/profile.html")
